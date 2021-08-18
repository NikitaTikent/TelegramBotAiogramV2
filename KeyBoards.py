from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import config


button_menu = InlineKeyboardButton('Меню', callback_data='menu')


def main_keyboard(id_user):
    button_cryptocurrency = InlineKeyboardButton('💼 Криптовалюты 💼', callback_data='cryptocurrency')
    button_wheater = InlineKeyboardButton('🌤 Погода 🌤', callback_data='weather')
    button_budget = InlineKeyboardButton('💰 Бюджет 💰', callback_data='budget')

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(button_cryptocurrency, button_wheater)

    if id_user == config.ADMIN_ID or id_user in config.FRIENDS:
        keyboard.add(button_budget)

    return keyboard


# ---------------------------------------------------------------------------------------


button_budget_history = InlineKeyboardButton('🗄 История 🗄', callback_data='budget_history')
button_entertainment = InlineKeyboardButton('🖋 Добавить 🖋', callback_data='budget_add')

budget_keyboard = InlineKeyboardMarkup(row_width=1)
budget_keyboard.add(button_budget_history,button_entertainment, button_menu)


# ---------------------------------------------------------------------------------------


button_need = InlineKeyboardButton('🛒 Незапланированные 🛒', callback_data='budget_need')
button_entertainment = InlineKeyboardButton('🎉 Развлечения 🎉', callback_data='budget_entertainment')

category_keyboard = InlineKeyboardMarkup(row_width=1)
category_keyboard.add(button_need, button_entertainment, button_menu)


# ---------------------------------------------------------------------------------------


def cryptocurrency(id_user):
    button_admin_Eth = KeyboardButton('📊 Ethereum 📊')   # Отключена из-за продажи крипты

    button_history = InlineKeyboardButton('💾 История 💾', callback_data='history')
    button_calculation = InlineKeyboardButton('📈 Расчет 📈', callback_data='calculation')
    button_admin_XRP = InlineKeyboardButton('📊 XRP 📊', callback_data='admin_XRP')
    button_rates = InlineKeyboardButton('📊 Курсы 📊', callback_data='rates')


    keyboard = InlineKeyboardMarkup(row_width=1)

    if id_user == config.ADMIN_ID:
        keyboard.add(button_admin_XRP)

    keyboard.add(button_calculation, button_rates, button_history, button_menu)
    
    return keyboard
# -------------------------------Выбор криптовалюты-------------------------------------


button_Ethereum_check = InlineKeyboardButton('Ethereum', callback_data='check_eth')
button_XRP_check = InlineKeyboardButton('XRP', callback_data='check_xrp')
button_Bitcoin_check = InlineKeyboardButton('Bitcoin', callback_data='check_btc')

AnswerPostKeyboard = InlineKeyboardMarkup(row_width=2)
AnswerPostKeyboard.add(button_Ethereum_check, button_XRP_check, button_Bitcoin_check)
AnswerPostKeyboard.add(button_menu)
# ---------------------------------------------------------------------------------------


button_left_message = InlineKeyboardButton('Закрепить', callback_data='fix_message')

ChekKeyboard = InlineKeyboardMarkup(row_width=1)
ChekKeyboard.add(button_left_message, button_menu)
# -----------------------------------Выход в меню----------------------------------------


ComeBack = InlineKeyboardMarkup(row_width=1)
ComeBack.add(button_menu)
