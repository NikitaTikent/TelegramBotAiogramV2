# свои
import KeyBoards
from Messages import Messages
import weather
from jarvis import Jarvis_handlers
from googlesheets import Jarvismember
from cryptocurrency import crypto_handlers
from budget import budget_handlers
import config
#
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

import time
import asyncio

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_message(message):
    user_id = message.from_user.id
    await bot.send_message(user_id, Messages['start'], reply_markup=KeyBoards.main_keyboard(user_id))


@dp.message_handler(commands=['help'])
async def start_message(message):
    user_id = message.from_user.id
    await bot.send_message(user_id, Messages['help_message'], reply_markup=KeyBoards.ComeBack)


@dp.callback_query_handler(lambda c: c.data == 'menu', state='*')
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await bot.edit_message_text(Messages['start'], callback.from_user.id, callback.message.message_id,
                                reply_markup=KeyBoards.main_keyboard(user_id))


@dp.callback_query_handler(lambda c: c.data == 'weather')
async def ForMyMany(callback: types.CallbackQuery):
    Jarvismember().new_user(callback)   # проверка новый ли пользователь
    text = weather.weather_messages() # return text of weather message
    await bot.edit_message_text(text, callback.from_user.id,
                                callback.message.message_id, reply_markup=KeyBoards.ComeBack)



async def remember_func():
    while True:
        result = []
        # time_now = float(time.strftime("%M.%S", time.localtime()))    # for test
        timer = str(int(time.strftime("%H", time.localtime()))+5)+time.strftime(".%d.%m", time.localtime())
        time_now = float(time.strftime("%H.%M%S", time.localtime()))+5    # Разница с сервером 5 часов
        if time_now % 2 == 0 or time_now % 2 == 1:
            data = Jarvismember().load_all()
            data_date = [i for i in data['values'][1:]]
            for i in data_date:
                if timer == str(i[1]):   # timer
                    text = i[3]+', напоминаю: '+i[2]
                    result.append([i[0], text])
            if len(result) > 0:
                for i in result:
                    await bot.send_message(i[0], i[1])
                result = []
            await asyncio.sleep(1)
        await asyncio.sleep(0)


if __name__ == '__main__':
    crypto_handlers(bot, dp)
    budget_handlers(bot, dp)
    Jarvis_handlers(bot, dp)
    loop = asyncio.get_event_loop()
    loop.create_task(remember_func())
    executor.start_polling(dp)
