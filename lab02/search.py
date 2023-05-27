from enum import Enum
from math import ceil
from typing import Optional

from aiogram import Router
from aiogram.filters import Text
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InputMediaPhoto, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import api


SEARCH_PAGE_SIZE = 4
FACILITY_PAGE_SIZE = 4


router = Router()


class ItemCallbackData(CallbackData, prefix='item'):
    id: str


class PaginationDirection(str, Enum):
    next = 'next'
    previous = 'prev'


class ItemPaginationCallbackData(CallbackData, prefix='item_pagination'):
    direction: Optional[PaginationDirection] = None


class FacilityPaginationCallbackData(CallbackData, prefix='fac_pagination'):
    direction: Optional[PaginationDirection] = None


@router.message(Text(startswith=''))
async def search(message: Message, state: FSMContext):
    assert message.text != None

    data = await state.get_data()
    city: str | None = data['city']
    if city == None:
        await message.reply('Перед поиском необходимо указать ваш город')
        return

    result = api.search(message.text, api.SearchOptions(city))
    if len(result) == 0:
        await message.reply('Не удалось найти лекарства по вашему запросу')
        return

    builder = InlineKeyboardBuilder()
    media = []
    for i in range(min(SEARCH_PAGE_SIZE, len(result))):
        data = ItemCallbackData(id=result[i].id)
        builder.row(InlineKeyboardButton(text=result[i].name,
                                         callback_data=data.pack()))
        media.append(InputMediaPhoto(media=result[i].href)) # pyright: ignore[reportGeneralTypeIssues]

    page = '1/' + str(ceil(result.count / SEARCH_PAGE_SIZE))
    builder.row(
        InlineKeyboardButton(text='<<',
            callback_data=ItemPaginationCallbackData(direction=PaginationDirection.previous).pack()),
        InlineKeyboardButton(text=page,
            callback_data=ItemPaginationCallbackData().pack()),
        InlineKeyboardButton(text='>>',
            callback_data=ItemPaginationCallbackData(direction=PaginationDirection.next).pack())
    )

    await message.reply_media_group(media)
    await message.answer(f'Найдено {result.count} товаров',
                         reply_markup=builder.as_markup())

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

    result = api.get_facilities(callback_data.id, api.FacilityOptions(city, 1))
    if result.count == 0:
        await callback.answer('Не удалось найти адреса!')
        return

    text = f'Найдено {result.count} адресов\n'
    for i in range(min(FACILITY_PAGE_SIZE, len(result))):
        text += f'\n{i + 1}) {result[i].name}, {result[i].address}\n'

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='<<',
            callback_data=FacilityPaginationCallbackData(direction=PaginationDirection.previous).pack()),
        InlineKeyboardButton(text='1/' + str(ceil(result.count / FACILITY_PAGE_SIZE)),
            callback_data=FacilityPaginationCallbackData().pack()),
        InlineKeyboardButton(text='>>',
            callback_data=FacilityPaginationCallbackData(direction=PaginationDirection.next).pack()),
    )

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(ItemPaginationCallbackData.filter())
async def callback_item_pagination(
    callback: CallbackQuery,
    callback_data: ItemPaginationCallbackData,
    state: FSMContext
):
    assert callback.message != None
    print('item_pagination')
    await callback.answer()


@router.callback_query(FacilityPaginationCallbackData.filter())
async def callback_facility_pagination(
    callback: CallbackQuery,
    callback_data: FacilityPaginationCallbackData,
    state: FSMContext
):
    assert callback.message != None
    print('facility_pagination')
    await callback.answer()
