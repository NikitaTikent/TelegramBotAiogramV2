from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_hi = KeyboardButton('📈 Расчет 📈')
button_by = KeyboardButton('📊 Курсы 📊')
Free_kb = ReplyKeyboardMarkup(resize_keyboard=True)
Free_kb.add(button_hi, button_by)


button_admin_Eth = KeyboardButton('📊 Etherium 📊')
button_admin_XRP = KeyboardButton('📊 XRP 📊')
Admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
Admin_kb.add(button_hi, button_by, button_admin_Eth, button_admin_XRP)
# ---------------------------------------------------------------------------------------

button_inline_1 = InlineKeyboardButton('Etherium', callback_data='button1')
button_inline_2 = InlineKeyboardButton('XRP', callback_data='button2')
button_inline_3 = InlineKeyboardButton('Bitcoin', callback_data='button3')

AnswerPostKeyboard = InlineKeyboardMarkup(row_width=1)
AnswerPostKeyboard.add(button_inline_1, button_inline_2, button_inline_3)
# ---------------------------------------------------------------------------------------


button_inline_21 = InlineKeyboardButton('Оставить', callback_data='button21')
button_inline_22 = InlineKeyboardButton('Удалить', callback_data='button22')

ChekKeyboard = InlineKeyboardMarkup(row_width=1)
ChekKeyboard.add(button_inline_21, button_inline_22)
# ---------------------------------------------------------------------------------------
