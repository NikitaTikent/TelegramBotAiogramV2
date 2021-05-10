from parsers import USD_Price, CryptoRates
# Клавиатура
import KeyBoards
#
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import time
import asyncio

storage = MemoryStorage()
bot = Bot(token='')
dp = Dispatcher(bot, storage=storage)


@dp.callback_query_handler(lambda c: c.data == 'button21')
async def First_callback_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=None)


@dp.callback_query_handler(lambda c: c.data == 'button22')
async def First_callback_handler(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


# States
class Form(StatesGroup):
    CryptoAsk = State()


def Osnova(type_crypto, My):
    USDprice = USD_Price()
    CryptoPrice = CryptoRates()

    text_def = """\
    Курс Криптовалюты: ${}
    \n {} ({}) -> {} Р 
    """
    if type_crypto == 'Eth':
        Result = round((float(CryptoPrice[2]) * float(USDprice) * float(My)), 1)
        Out = text_def.format(CryptoPrice[2], My, 'Eth', Result)
    elif type_crypto == 'XRP':
        Result = round((float(CryptoPrice[0]) * float(USDprice) * float(My)), 1)
        Out = text_def.format(CryptoPrice[0], My, 'XRP', Result)
    elif type_crypto == 'Bitcoin':
        Result = round((float(CryptoPrice[1]) * float(USDprice) * float(My)), 1)
        Out = text_def.format(CryptoPrice[1], My, 'Bitcoin', Result)
    else:
        Out = 'Error'
    return Out


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['run'])
async def process_start_command(message: types.Message):
    if message.from_user.id == 1:
        await message.reply("Привет!", reply_markup=KeyBoards.Admin_kb)
    else:
        await message.reply("Привет!", reply_markup=KeyBoards.Free_kb)
    await bot.delete_message(message.from_user.id, message.message_id)


@dp.message_handler(regexp='📊 Etherium 📊')
async def ForMyMany(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    if message.from_user.id == 1:
        await bot.send_message(message.from_user.id, Osnova('Eth', 1), reply_markup=KeyBoards.ChekKeyboard)
    else:
        await bot.send_message(message.from_user.id, 'Ошибка Доступа')


@dp.message_handler(regexp='📊 XRP 📊')
async def ForMyMany(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    if message.from_user.id == 1:
        await bot.send_message(message.from_user.id, Osnova('XRP', 1), reply_markup=KeyBoards.ChekKeyboard)
    else:
        await bot.send_message(message.from_user.id, 'Ошибка Доступа')


@dp.message_handler(regexp='📊 Курсы 📊')
async def Crypto_Rates(message: types.Message):
    USDprice = USD_Price()
    await bot.delete_message(message.from_user.id, message.message_id)
    text_def = """\
        Курс Bitcoin: ${}
        \nКурс XRP: ${}
        \nКурс Etherium: ${}
        \nКурс USD: {} ₽
        """
    XRPPrice, BitcoinPrice, EtheriumPrice = CryptoRates()
    Out = text_def.format(BitcoinPrice, XRPPrice, EtheriumPrice, USDprice)
    await bot.send_message(message.from_user.id, Out, reply_markup=KeyBoards.ChekKeyboard)


@dp.message_handler(regexp='📈 Расчет 📈')
async def ForMyMany(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите криптовалюту:', reply_markup=KeyBoards.AnswerPostKeyboard)


@dp.callback_query_handler(lambda c: c.data == 'button1')   # Etherium
async def First_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = 'Eth'
        data['for_delete-1'] = callback_query.message.message_id
    await Form.CryptoAsk.set()
    await bot.edit_message_text('Количество выбранной криптовалюты:', chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id, reply_markup=None)


@dp.callback_query_handler(lambda c: c.data == 'button2')   # XRP
async def First_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = 'XRP'
        data['for_delete-1'] = callback_query.message.message_id
    await Form.CryptoAsk.set()
    await bot.edit_message_text('Количество выбранной криптовалюты:', chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id, reply_markup=None)


@dp.callback_query_handler(lambda c: c.data == 'button3')   # Bitcoin
async def First_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = 'Bitcoin'
        data['for_delete-1'] = callback_query.message.message_id
    await Form.CryptoAsk.set()
    await bot.edit_message_text('Количество выбранной криптовалюты:', chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id, reply_markup=None)


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Cancelled.', reply_markup=KeyBoards.ChekKeyboard)


@dp.message_handler(state=Form.CryptoAsk)
async def Raschet_Crypto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        name = data['name']
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.delete_message(message.from_user.id, data['for_delete-1'])
    try:
        Result = Osnova(name, float(message.text.replace(',', '.')))
        await bot.send_message(message.chat.id, Result, reply_markup=KeyBoards.ChekKeyboard)
    except:
        await bot.send_message(message.chat.id, 'Введено неверное значение!', reply_markup=KeyBoards.ChekKeyboard)
    await state.finish()


async def OurNotice():
    while True:
        time_now = float(time.strftime("%H.%M", time.localtime()))
        if 1 <= time_now <= 12:
            if time_now % 2 == 0 or time_now % 2 == 1:
                await bot.send_message(1, Osnova('Eth', 1))
                await asyncio.sleep(65)
        await asyncio.sleep(1)
        # Внесены правки для проверки минут, теперь перезапуск не играет роли


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(OurNotice())
    executor.start_polling(dp)
