import KeyBoards
import Messages as msg
from Messages import Messages
import weather
from parsers import MainParser
from googlesheets import Jarvismember
from States import Form
from moder import moderate
import config

import time
import random

from aiogram import types
from aiogram.dispatcher import FSMContext

welcom = ['прив', 'здоров', 'здаров', 'шалом']


def Jarvis_handlers(bot, dp):
	@dp.message_handler()
	async def jarvis(message: types.Message, state: FSMContext):
		Jarvismember().new_user(message)
		if moderate(message):  # удаляет мат
			await bot.delete_message(message.chat.id, message. message_id)
		else:
			answer = Jarvis.answer(message)
			if answer:
				if answer[0] == 'Когда?':
					async with state.proxy() as data:
						data['forremembertext'] = answer[1]
					await Form.RememberAsk.set()
					format_remember = '\nУкажите время в формате чч.дд.мм'
					await bot.send_message(message.chat.id, answer[0]+format_remember)
				if answer[0] != 'Когда?':
					await bot.send_message(message.chat.id, answer)


	@dp.message_handler(state=Form.RememberAsk)
	async def Raschet_Crypto(message: types.Message, state: FSMContext):
	    chat_id = message.chat.id
	    user_name = message.from_user.first_name
	    message_text = message.text

	    async with state.proxy() as data:
	        text = data['forremembertext']

	    save = Jarvismember().save_new_jarvis_remember(chat_id, message_text, text, user_name)

	    if save:
	        await bot.send_message(message.chat.id, msg.remember_answer())
	    else:
	        await bot.send_message(message.chat.id, 'Error')

	    await state.finish()

	@dp.message_handler(content_types=['audio'])	#For Music
	async def start_message(message):
		id_message = message.message_id
		chat_id = message.chat.id
		await bot.delete_message(chat_id, id_message)
		await bot.send_audio(config.MUSIC_CHAT_ID, message.audio.file_id)



class Jarvis:
	def answer(message):
		user_name = message.from_user.first_name
		text = message.text.lower()
		chat_id = message.chat.id
		user_id = message.from_user.id
		
		answer = ""

		if 'джарвис' == text:
			answer = 'Приветствую, {}'.format(user_name)
			return answer
		if 'время сервера' == text:
			answer = time.strftime("%H.%M", time.localtime())
			return answer
		if 'джарвис' in text:
			# проверка приветствия
			for x in welcom:
				if x in text:
					answer += 'Приветствую, {}'.format(user_name)
			# проверка запроса погоды
			if 'погод' in text:
				weather_result = weather.weather_messages()	# return text of weather message
				if weather_result:
					answer += weather_result
				else:
					return 'Ошибка загрузки погоды'
			# Для напоминания
			if 'напомни' in text:
				for_delete_from_message = ['джарвис', 'напомни', 'что', ',', 'мне', 'пожалуйста']
				for i in for_delete_from_message:
					text = text.replace(i, '')
				return ['Когда?', text]

			# Чтобы послал всех
			if ('пошли всех' in text) or ('пошли их' in text):
				if user_id == config.ADMIN_ID:
					answer += Messages['fuck_off']
				else:
					answer += '\nСам пошел'

			# Выбирает случайного человека из беседы
			if 'выбери жертву' in text:
				name_list = []
				all_users = Jarvismember().load_users()
				for i in all_users['values']:
					if str(chat_id) == i[2]:
						name_list.append(i[1])
				answer = random.choice(name_list)

			# Выбирает случайного человека из беседы
			if 'что ты умеешь' in text:
				answer = msg.what_i_can(user_id)
			return answer
		return False
