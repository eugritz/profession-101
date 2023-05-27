from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from api import get_cities


router = Router()
cities = get_cities()


class Form(StatesGroup):
    city = State()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Привет, я бот MedFind!\n' +
                         'Я помогаю пользователям в поиске лекарств по их названию')
    await state.set_state(Form.city)
    await cmd_city(message, no_reply=True)


@router.message(Command('city'))
async def cmd_city(message: Message, no_reply=False):
    text = 'Пожалуйста, введите название города'
    if no_reply:
        await message.answer(text)
    else:
        await message.reply(text)


@router.message(Command('cancel'), StateFilter('*'))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.reply('Операция отменена')


@router.message(Form.city, Text(startswith=''))
async def process_city(message: Message, state: FSMContext):
    assert message.text != None
    success = False
    for city in cities:
        if city.name.lower() == message.text.lower():
            await state.update_data(city=city.id)
            success = True
            break

    buttons = [
        [KeyboardButton(text='Поиск')],
        [KeyboardButton(text='Изменить город')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Введите название лекарства'
    )

    if success:
        answer = 'Город успешно задан!\n' + \
                 'Для поиска лекарств просто напишите сообщение в этом чате'
    else:
        answer = 'Мы не нашли город с таким названием.\n' + \
                 'Для поиска лекарств необходимо выбрать город'

    await message.answer(answer, reply_markup=keyboard)
    await state.set_state(state=None)


@router.message(Text('Поиск'))
async def btn_search(message: Message):
    await message.reply('Пожалуйста, введите название лекарства')


@router.message(Text('Изменить город'))
async def btn_change_city(message: Message):
    await cmd_city(message)
