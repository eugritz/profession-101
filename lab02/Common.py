from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import AptsApi as api
from math import ceil

SEARCH_PAGE_SIZE = 4
FACILITY_PAGE_SIZE = 4


class Form(StatesGroup):
    city = State()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_city, commands='city')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')

    dp.register_message_handler(process_city, state=Form.city)
    dp.register_message_handler(btn_search, Text('Поиск'))
    dp.register_message_handler(btn_change_city, Text('Изменить город'))

    dp.register_message_handler(search)
    dp.register_callback_query_handler(callback_select)


async def cmd_start(message: types.Message):
    await message.answer('Привет, я бот MedFind!\n' +
                         'Я помогаю пользователям в поиске лекарств по их названию')
    await cmd_city(message, no_reply=True)


async def cmd_city(message: types.Message, no_reply=False):
    text = 'Пожалуйста, введите название города'
    if no_reply:
        await message.answer(text)
    else:
        await message.reply(text)
    await Form.city.set()


async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Операция отменена')


async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

    buttons = [
        [types.KeyboardButton(text='Поиск')],
        [types.KeyboardButton(text='Изменить город')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Введите название лекарства'
    )

    answer = 'Город успешно задан!\n' + \
             'Для поиска лекарств просто напишите сообщение в этом чате'

    await message.answer(answer, reply_markup=keyboard)
    await state.set_state(state=None)


async def btn_search(message: types.Message):
    await message.reply('Пожалуйста, введите название лекарства')


async def btn_change_city(message: types.Message):
    await cmd_city(message)


async def search(message: types.Message, state: FSMContext):
    city: str | None = None
    async with state.proxy() as data:
        city = data['city']
    if city == None:
        await message.reply('Перед поиском необходимо указать ваш город')
        return

    result = api.search(message.text, api.SearchOptions(city))
    if len(result) == 0:
        await message.reply('Не удалось найти лекарства по вашему запросу')
        return

    keyboard = types.InlineKeyboardMarkup()
    media = []
    for i in range(min(SEARCH_PAGE_SIZE, len(result))):
        keyboard.add(types.InlineKeyboardButton(text=result[i].name,
                                                callback_data=result[i].id))
        media.append(types.InputMediaPhoto(result[i].href))

    keyboard.row(types.InlineKeyboardButton(text='<<',
                                            callback_data='left_search'),
                 types.InlineKeyboardButton('1/' + str(ceil(result.count / SEARCH_PAGE_SIZE)),
                                            callback_data='middle_search'),
                 types.InlineKeyboardButton('>>',
                                            callback_data='right_search'))

    await message.reply_media_group(media)
    await message.answer(f'Найдено {result.count} запись(ей)', reply_markup=keyboard)

async def callback_select(call: types.CallbackQuery, state: FSMContext):
    city: str | None = None
    async with state.proxy() as data:
        city = data['city']
    if city == None:
        return

    id = call.data
    result = api.get_facilities(id, api.FacilityOptions(city, 1))

    text = f'Найдено {result.count} запись(ей)\n'
    for i in range(min(FACILITY_PAGE_SIZE, len(result))):
        text += f'\n{i + 1}) {result[i].name}, {result[i].address}\n'

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text='<<',
                                            callback_data='left_facility'),
                 types.InlineKeyboardButton('1/' + str(ceil(result.count / FACILITY_PAGE_SIZE)),
                                            callback_data='middle_facility'),
                 types.InlineKeyboardButton('>>',
                                            callback_data='right_facility'))

    await call.message.answer(text, reply_markup=keyboard)
    await call.answer()
