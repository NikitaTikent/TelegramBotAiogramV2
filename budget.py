# свои
import KeyBoards
from Messages import Messages
from States import Form
from googlesheets import Budget
import config
# 

from aiogram import types
from aiogram.dispatcher import FSMContext


def budget_handlers(bot, dp):
    @dp.callback_query_handler(lambda c: c.data == 'budget')
    async def ForMyMany(callback: types.CallbackQuery):
        await bot.edit_message_text('Выберите раздел:', callback.from_user.id, callback.message.message_id,
                                    reply_markup=KeyBoards.budget_keyboard)


    @dp.callback_query_handler(lambda c: c.data == 'budget_history')
    async def ForMyMany(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        if user_id == config.ADMIN_ID:    # разные таблицы в гугле для меня и остальных
            result = Budget().load_all()['values']
        else:
            result = Budget('budget_users').load_all()['values']
            result = [i for i in result if i[3]==str(user_id)or i[3]=='user_id']
        text = ''
        if result[1:]:
            if len(result)>6:
                for i in result[len(result)-1:len(result)-5:-1]:
                    text += Messages['budget_history'].format(i[0], i[1], i[2])
            else:
                for i in result[len(result)-1:0:-1]:
                    text += Messages['budget_history'].format(i[0], i[1], i[2])
        else:
            text += 'Записи не найдены'
        await bot.edit_message_text(text, callback.from_user.id, callback.message.message_id,
                                    reply_markup=KeyBoards.ComeBack)


    @dp.callback_query_handler(lambda c: c.data == 'budget_add')
    async def ForMyMany(callback: types.CallbackQuery):
        await bot.edit_message_text('Выберите категорию:', callback.from_user.id, callback.message.message_id,
                                    reply_markup=KeyBoards.category_keyboard)
    

    @dp.callback_query_handler(lambda c: c.data.startswith('budget_'))
    async def Ethereum_check(callback_query: types.CallbackQuery, state: FSMContext):
        button_name = callback_query.data
        category = button_name[7:]
        async with state.proxy() as data:
            data['budget_category'] = category
        await Form.budget_summa.set()
        await bot.edit_message_text('Потраченная сумма:', chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, reply_markup=KeyBoards.ComeBack)


    @dp.message_handler(state=Form.budget_summa)
    async def Raschet_Crypto(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        async with state.proxy() as data:
            data['summa'] = message.text
        await Form.budget_name.set()
        await bot.send_message(message.chat.id, 'На что?', reply_markup=KeyBoards.ComeBack)


    @dp.message_handler(state=Form.budget_name)
    async def Raschet_Crypto(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        async with state.proxy() as data:
            summa = data['summa']
            category = data['budget_category']
        if user_id == config.ADMIN_ID:
            sheet = 'budget'
        else:
            sheet = 'budget_users'
        if Budget(sheet).add(category, message.text, summa, user_id):
            await bot.send_message(user_id, Messages['start'], reply_markup=KeyBoards.main_keyboard(user_id))
        else:
            await bot.send_message(message.chat.id, 'Ошибка записи', reply_markup=KeyBoards.ComeBack)
        await state.finish()
