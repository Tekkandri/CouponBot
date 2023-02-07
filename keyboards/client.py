from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from database import coupon_db

# ------start up markup------
start_up_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
registration_btn = KeyboardButton("Зарегистрироваться")
get_promo_btn = KeyboardButton("Получить промокод")
back_btn = KeyboardButton("Назад")
start_up_markup.add(registration_btn,get_promo_btn,back_btn)

# ------registration menu markup------
registration_markup = ReplyKeyboardMarkup(resize_keyboard=True)
exit_btn = KeyboardButton("Выход")
registration_markup.add(exit_btn, get_promo_btn)

# ------if user not exist markup------
reply_btn = KeyboardButton("Повторить")
wrong_enter_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(registration_btn,reply_btn,exit_btn)

# ------get promo menu markup------
get_promo_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(exit_btn, get_promo_btn)

# ------successful log in menu------
check_promo_btn = KeyboardButton("Посмотреть промокоды")
successful_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(exit_btn,check_promo_btn)

# ------promo list markup------
def get_promo():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = coupon_db.get_promo()
    for button in buttons:
        markup.add(KeyboardButton(button[0]))
    return markup.add(exit_btn)

# ------promo menu markup------
continue_btn = KeyboardButton("Продолжить")
promo_menu_markup = ReplyKeyboardMarkup(row_width= 1, resize_keyboard=True).add(continue_btn, exit_btn)