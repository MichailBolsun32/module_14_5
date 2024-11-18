import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions import *
from module_14_5_ import crud_functions

logging.basicConfig(level=logging.INFO)# настройка logov

all_products = get_all_products()

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

#Кнопки главного меню дополните кнопкой "Регистрация".

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Расчитать'),
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Регистрация')
        ]
    ], resize_keyboard=True # активировать автоматическое изменение размера клавиатуры
)

kb_calculate = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

kb_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
         ]
    ],resize_keyboard=True
)

#Напишите новый класс состояний RegistrationState с
# следующими объектами класса State: username, email, age, balance(по умолчанию 1000)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

#sing_up(message):

    # Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
    # Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
    # После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

#set_username(message, state):
    # Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
    # Если пользователя message.text ещё нет в таблице,
            # то должны обновляться данные в состоянии username на message.text.
            # Далее выводится сообщение "Введите свой email:"
            # и принимается новое состояние RegistrationState.email.
    # Если пользователь с таким message.text есть в таблице,
        # то выводить "Пользователь существует, введите другое имя" и
        # запрашивать новое состояние для RegistrationState.username.

@dp.message_handler(state = RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_include(message.text):
        await state.update_data(username=message.text)
        await message.answer(f"Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer(f"Пользователь существует, введите другое имя:")
        await RegistrationState.username.set()

#set_email(message, state):
    # Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
    # Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
    # Далее выводить сообщение "Введите свой возраст:":
    # После ожидать ввода возраста в атрибут RegistrationState.age.

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer(f"Введите свой возраст:")
    await RegistrationState.age.set()

# set_age(message, state):
#     Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
#     Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
#     Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users
        #     при помощи ранее написанной crud-функции add_user.
#     В конце завершать приём состояний при помощи метода finish().

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    data_u = data['username']
    data_e = data['email']
    data_a = int(data['age'])
    crud_functions.add_user(data['username'] ,data['email'], int(data['age']))
    await state.finish()
    await message.answer(f'Регистрация прошла успешно.', reply_markup=kb_start)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    number = 0
    await message.answer(f'Название: {all_products[number][1]} | Описание: {all_products[number][2]} '
                                       f'| Цена: {all_products[number][3]}')
    with open('prod_1.jpg', 'rb') as img:
       await message.answer_photo(img)
    number += 1
    await message.answer(f'Название: {all_products[number][1]} | Описание: {all_products[number][2]} '
                         f'| Цена: {all_products[number][3]}')
    with open('prod_2.jpg', 'rb') as img:
        await message.answer_photo(img)
    number += 1
    await message.answer(f'Название: {all_products[number][1]} | Описание: {all_products[number][2]} '
                         f'| Цена: {all_products[number][3]}')
    with open('prod_3.jpg', 'rb') as img:
        await message.answer_photo(img)
    number += 1
    await message.answer(f'Название: {all_products[number][1]} | Описание: {all_products[number][2]} '
                         f'| Цена: {all_products[number][3]}')
    with open('prod_4.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer(f'Выберите продукт для покупки:',reply_markup=kb_product)

@dp.callback_query_handler(text='product_buying')
async def get_formulas(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb_start)

@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_calculate)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('BMR=10×масса тела (кг)+6,25×рост (см)−5×возраст (годы)+5')

@dp.message_handler(text = 'Информация')
async def info_message(message):
    await message.answer('Я бот, помогающий твоему здоровью!')

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    bmr = int(data['weight']) * 10 + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.message_handler()
async def start_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)