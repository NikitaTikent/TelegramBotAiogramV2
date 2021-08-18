# свои
import KeyBoards
from Messages import Messages
from parsers import MainParser
from googlesheets import CryptoMember
from States import Form
# 
import pickle
from aiogram import types
from aiogram.dispatcher import FSMContext


def crypto_handlers(bot, dp):
    @dp.callback_query_handler(lambda c: c.data == 'cryptocurrency')
    async def ForMyMany(callback: types.CallbackQuery):
        id_user = callback.from_user.id
        with open('{}.data'.format(id_user), 'wb') as f:
            pickle.dump('', f)
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id,
                                            reply_markup=KeyBoards.cryptocurrency(id_user))

    @dp.callback_query_handler(lambda c: c.data == 'fix_message')
    async def fix_last_message(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        # save in google sheet
        CryptoMember.save_new_crypto_result(user_id)
        #
        await bot.edit_message_reply_markup(user_id, callback_query.message.message_id,
                                            reply_markup=None)
        await bot.send_message(user_id, Messages['start'], reply_markup=KeyBoards.main_keyboard(user_id))
    

    @dp.callback_query_handler(lambda c: c.data == 'rates')
    async def Crypto_Rates(callback: types.CallbackQuery):
        text = MainParser.cryptorates()
        await bot.edit_message_text(text, callback.from_user.id, callback.message.message_id,
                                    reply_markup=KeyBoards.ChekKeyboard)


    @dp.callback_query_handler(lambda c: c.data == 'history')
    async def Crypto_Rates(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        text = CryptoMember.searh_of_crypto(user_id)
        await bot.edit_message_text(text, callback.from_user.id, callback.message.message_id,
                                    reply_markup=KeyBoards.ComeBack)


    @dp.callback_query_handler(lambda c: c.data == 'calculation')
    async def ForMyMany(callback: types.CallbackQuery):
        await bot.edit_message_text('Выберите криптовалюту:', callback.from_user.id, callback.message.message_id,
                                    reply_markup=KeyBoards.AnswerPostKeyboard)


    @dp.message_handler(state=Form.CryptoAsk)
    async def Raschet_Crypto(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        async with state.proxy() as data:
            name = data['name']
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.delete_message(message.from_user.id, data['for_delete-1'])
        try:
            Result = MainParser.osnova(user_id, name, float(message.text.replace(',', '.')))
            await bot.send_message(message.chat.id, Result, reply_markup=KeyBoards.ChekKeyboard)
        except:
            await bot.send_message(message.chat.id, 'Введено неверное значение!', reply_markup=KeyBoards.ChekKeyboard)
        await state.finish()


    @dp.callback_query_handler(lambda c: c.data == 'admin_XRP')
    async def ForMyMany(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        text = MainParser.osnova(user_id, 'xrp', 20)
        await bot.edit_message_text(text, user_id, callback.message.message_id,
                                    reply_markup=KeyBoards.ChekKeyboard)


    @dp.callback_query_handler(lambda c: c.data.startswith('check'))
    async def Ethereum_check(callback_query: types.CallbackQuery, state: FSMContext):
        button_name = callback_query.data
        if button_name.startswith('check'):
            crypto_name = button_name[6:]
            async with state.proxy() as data:
                data['name'] = crypto_name
                data['for_delete-1'] = callback_query.message.message_id
            await Form.CryptoAsk.set()
            await bot.edit_message_text('Количество выбранной криптовалюты:', chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, reply_markup=KeyBoards.ComeBack)
