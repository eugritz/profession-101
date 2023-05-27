from enum import Enum
from math import ceil
from typing import Optional
from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageMedia
from aiogram.types import InlineKeyboardButton, InputMediaPhoto, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import api
from pagination import paginate


SEARCH_PAGE_SIZE = 4
FACILITY_PAGE_SIZE = 4


router = Router()


class ItemCallbackData(CallbackData, prefix='item'):
    id: str


class PaginationDirection(str, Enum):
    next = 'next'
    previous = 'prev'


class ItemPaginationCallbackData(CallbackData, prefix='item_pag'):
    query: Optional[str] = None
    page: Optional[int] = None
    album_ids: Optional[str] = None


class FacilityPaginationCallbackData(CallbackData, prefix='fac_pag'):
    id: Optional[str] = None
    page: Optional[int] = None


@router.message(Text(startswith=''))
async def search(message: Message, state: FSMContext):
    assert message.text != None

    data = await state.get_data()
    city: str | None = data['city']
    if city == None:
        await message.reply('Перед поиском необходимо указать ваш город')
        return

    query = message.text
    result = api.search(query, api.SearchOptions(city))
    if len(result) == 0:
        await message.reply('Не удалось найти лекарств по вашему запросу')
        return

    media = []
    for i in range(min(SEARCH_PAGE_SIZE, len(result))):
        media.append(InputMediaPhoto(media=result[i].preview_image_source)) # pyright: ignore[reportGeneralTypeIssues]
    album = await message.reply_media_group(media)
    album_ids = [str(msg.message_id) for msg in album]

    builder = InlineKeyboardBuilder()
    for i in range(min(SEARCH_PAGE_SIZE, len(result))):
        data = ItemCallbackData(id=result[i].id[:59])
        builder.row(
            InlineKeyboardButton(
                text=result[i].name,
                callback_data=data.pack(),
            )
        )

    page_count = ceil(result.count / SEARCH_PAGE_SIZE)

    keyboard1 = builder.as_markup()
    keyboard2 = get_items_keyboard(query, ','.join(album_ids), 1, page_count)
    keyboard1.inline_keyboard.extend(keyboard2.inline_keyboard)
    await message.answer(f'Найдено {result.count} товаров', reply_markup=keyboard1)


@router.callback_query(ItemCallbackData.filter())
async def callback_item_select(
    callback: CallbackQuery,
    callback_data: ItemCallbackData,
    state: FSMContext
):
    assert callback.message != None
    data = await state.get_data()
    city: str | None = data['city']
    if city == None:
        return
    item_id = callback_data.id

    await callback.answer('Получение записей, это может занять некоторое время')
    result = api.get_facilities(item_id, api.FacilityOptions(city, 1))
    if result.count == 0:
        await callback.answer('Не удалось найти адреса!')
        return

    text = f'Найдено {result.count} адресов\n'
    for i in range(min(FACILITY_PAGE_SIZE, len(result))):
        text += f'\n{i + 1}) {result[i].name}, {result[i].address}\n'

    page_count = ceil(result.count / FACILITY_PAGE_SIZE)
    keyboard = get_facilities_keyboard(item_id, 1, page_count)
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(ItemPaginationCallbackData.filter())
async def callback_item_pagination(
    callback: CallbackQuery,
    callback_data: ItemPaginationCallbackData,
    state: FSMContext
):
    if callback_data.query == None:
        await callback.answer()
        return
    assert callback_data.page != None
    assert callback_data.album_ids != None

    assert callback.message != None
    assert callback.message.reply_markup != None
    data = await state.get_data()
    city: str | None = data['city']
    if city == None:
        return
    query = callback_data.query
    page = callback_data.page
    album_ids_raw = callback_data.album_ids
    album_ids = [int(id) for id in album_ids_raw.split(',')]

    await callback.answer('Получение записей, это может занять некоторое время')
    actual_page = (page * SEARCH_PAGE_SIZE - 1) // api.MAX_SEARCH_RESULTS_COUNT + 1
    print(actual_page)
    result = api.search(query, api.SearchOptions(city, page=actual_page))
    filtered = paginate(result, (page - 1) % 5, SEARCH_PAGE_SIZE)

    builder = InlineKeyboardBuilder()
    for i in range(min(SEARCH_PAGE_SIZE, len(filtered))):
        data = ItemCallbackData(id=filtered[i].id[:59])
        builder.row(InlineKeyboardButton(text=filtered[i].name,
                                         callback_data=data.pack()))
        media = InputMediaPhoto(media=filtered[i].preview_image_source) # pyright: ignore[reportGeneralTypeIssues]
        with suppress(TelegramBadRequest):
            await EditMessageMedia(
                chat_id=callback.message.chat.id,
                message_id=album_ids[i],
                media=media
            )

    page_count = ceil(result.count / SEARCH_PAGE_SIZE)
    keyboard1 = builder.as_markup()
    keyboard2 = get_items_keyboard(query, album_ids_raw, page, page_count)
    keyboard1.inline_keyboard.extend(keyboard2.inline_keyboard)
    await callback.message.edit_reply_markup(reply_markup=keyboard1)


@router.callback_query(FacilityPaginationCallbackData.filter())
async def callback_facility_pagination(
    callback: CallbackQuery,
    callback_data: FacilityPaginationCallbackData,
    state: FSMContext
):
    if callback_data.id == None:
        await callback.answer()
        return
    assert callback_data.page != None

    assert callback.message != None
    assert callback.message.reply_markup != None
    data = await state.get_data()
    city: str | None = data['city']
    if city == None:
        return
    page = callback_data.page
    item_id = callback_data.id

    await callback.answer('Получение записей, это может занять некоторое время')
    result = api.get_facilities(item_id, api.FacilityOptions(city, 1))
    filtered = paginate(result, page - 1, FACILITY_PAGE_SIZE)

    text = f'Найдено {result.count} адресов\n'
    for i in range(min(FACILITY_PAGE_SIZE, len(filtered))):
        n = (page - 1) * FACILITY_PAGE_SIZE + i + 1
        text += f'\n{n}) {filtered[i].name}, {filtered[i].address}\n'

    page_count = ceil(result.count / FACILITY_PAGE_SIZE)
    keyboard = get_facilities_keyboard(item_id, page, page_count)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


def get_items_keyboard(query: str, album: str, page: int, page_count: int):
    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(
            text='<<',
            callback_data=ItemPaginationCallbackData(
                query=query,
                page=page - 1,
                album_ids=album
            )
        )
    builder.button(
        text=f'{page}/{page_count}',
        callback_data=ItemPaginationCallbackData()
    )
    if page < page_count:
        builder.button(
            text='>>',
            callback_data=ItemPaginationCallbackData(
                query=query,
                page=page + 1,
                album_ids=album
            ).pack()
        )
    return builder.as_markup()


def get_facilities_keyboard(id: str, page: int, page_count: int):
    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(
            text='<<',
            callback_data=FacilityPaginationCallbackData(
                id=id,
                page=page - 1
            )
        )
    builder.button(
        text=f'{page}/{page_count}',
        callback_data=FacilityPaginationCallbackData()
    )
    if page < page_count:
        builder.button(
            text='>>',
            callback_data=FacilityPaginationCallbackData(
                id=id,
                page=page + 1
            ).pack()
        )
    return builder.as_markup()
