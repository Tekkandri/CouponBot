import keyboards.client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

import re

from create import bot
from keyboards.client import start_up_markup, registration_markup, wrong_enter_markup, get_promo_markup, get_promo, successful_menu_markup, promo_menu_markup
from database import coupon_db

WELCOME_MESSGE = """_Здравтсвуйте\!_ Вас приветсвует couponbot\.
Здесь вы можете ознакомиться с возможностями *бота*\.
Заказать такого же бота вы можете у [меня](https://t.me/Tekkanskiy)"""

GET_FIO = """_Введите, пожалуйста Вашу_ _*Фамилию, Имя и Отчество*_
*без* пробелов, запятых, кавычек и т\.п
Не спешите"""
GET_NUMBER = """_Введите Ваш номер телефона_
Формат: *7XXXXXXXXXX*"""
NUMBER_ERROR_MESSAGE = """Введите корректный номер"""

OUT_OF_COUPON = "Извините, нет доступных промокодов"
ERROR_OF_LOG_IN = "Ваш номер телефона не найден в базе. Пожалуйста, зарегистрируйтесь"

USER_MENU_MESSAGE = "Для просмотра промокода нажмите на интересующий вас магазин, сервис, услугу"

class FSMclient(StatesGroup):
    start = State()

    registration = State()
    fio = State()
    number = State()

    log_in = State()
    promo = State()

# ------exit------
async def exit_command(msg: types.Message, state: FSMContext):
    await state.finish()
    await start_menu(msg)


# ------start------
async def start_menu(msg: types.Message):
    await FSMclient.start.set()
    await bot.send_message(msg.from_user.id,WELCOME_MESSGE, reply_markup=start_up_markup, parse_mode="MarkdownV2")

# ------registration------
async def registration_menu(msg: types.Message):
    await FSMclient.registration.set()
    await bot.send_message(msg.from_user.id,GET_FIO, reply_markup=registration_markup, parse_mode="MarkdownV2")

async def get_fio(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["FIO"] = msg.text
        await msg.answer(GET_NUMBER,reply_markup=registration_markup, parse_mode="MarkdownV2")
        await FSMclient.fio.set()

async def get_number(msg: types.Message, state: FSMContext):
        regexp = re.compile('7\d{10}')
        if regexp.findall(msg.text):
            async with state.proxy() as data:
                data["number"] = msg.text
                coupon_db.registration(msg.from_user.id,data["FIO"],data["number"])
            await bot.send_message(msg.from_user.id, data["FIO"]+"!\nВы успешно зарегистрировались",reply_markup=registration_markup)
            await start_menu(msg)
        else:
            await msg.answer(NUMBER_ERROR_MESSAGE,reply_markup=registration_markup)

# ------log in------
async def log_in_menu(msg: types.Message):
    await FSMclient.log_in.set()
    await bot.send_message(msg.from_user.id,GET_NUMBER, reply_markup=get_promo_markup, parse_mode="MarkdownV2")

async def check_number(msg: types.Message):
    regexp = re.compile('7\d{10}')
    if regexp.findall(msg.text):
        user = coupon_db.check_registration(int(msg.text))
        if(len(user)>0):
            await bot.send_message(msg.from_user.id,f"""_Здравствуйте_, _*{user[0][1]}*_\. 
Здесь вы можете посмотреть *свои* промокоды\.
_Выберите следующее действие\._""", reply_markup=successful_menu_markup, parse_mode="MarkdownV2")
        else:
            await bot.send_message(msg.from_user.id,OUT_OF_COUPON, reply_markup=successful_menu_markup)
    else:
        await bot.send_message(msg.from_user.id, ERROR_OF_LOG_IN, reply_markup=wrong_enter_markup)

# ------user menu------
async def check_promo(msg: types.Message):
    await FSMclient.promo.set()
    await bot.send_message(msg.from_user.id, USER_MENU_MESSAGE, reply_markup=get_promo())

# ------promo menu------
async def promo_menu(msg: types.Message):
    data = coupon_db.get_description(msg.text)
    await bot.send_message(msg.from_user.id, f"""
*Поздравляем! Ваш промокод* _*{data[2]}*_
*{data[1]}*""", reply_markup=promo_menu_markup, parse_mode="MarkdownV2")

def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(start_menu,commands=["start"])
    dp.register_message_handler(exit_command, lambda msg: msg.text == "Выход", state="*")

    dp.register_message_handler(log_in_menu, lambda msg: msg.text == "Получить промокод" or msg.text == "Повторить", state="*")
    dp.register_message_handler(check_number, lambda msg: msg.text != "Получить промокод" and msg.text !="Повторить" and msg.text != "Выход" and msg.text != "Зарегистрироваться" and msg.text != "Посмотреть промокоды",state=FSMclient.log_in)

    dp.register_message_handler(registration_menu, lambda msg: msg.text == "Зарегистрироваться",state="*")
    dp.register_message_handler(get_fio, lambda msg: msg.text != "Получить промокод" and msg.text != "Повторить" and msg.text != "Выход" and msg.text != "Зарегистрироваться" and msg.text != "Посмотреть промокоды",state=FSMclient.registration)
    dp.register_message_handler(get_number, lambda msg: msg.text != "Получить промокод" and msg.text != "Повторить" and msg.text != "Выход" and msg.text != "Зарегистрироваться" and msg.text != "Посмотреть промокоды",state=FSMclient.fio)

    dp.register_message_handler(check_promo, lambda msg:msg.text == "Посмотреть промокоды" or msg.text == "Посмотреть промокоды", state=[FSMclient.log_in, FSMclient.promo])
    dp.register_message_handler(promo_menu, lambda msg: True, state=FSMclient.promo)