import random
import config

start_message = 'Привет! Этот бот поможет тебе узнать курсы криптовалют, ' \
                'умеет конвертировать их стоимости в рубли и бонусом показывает погоду'

rates = text_def = """\
        Курс Bitcoin: ${}
        \nКурс XRP: ${}
        \nКурс Etherium: ${}
        \nКурс USD: {} ₽
        """

convert_result = """\
                Курс Криптовалюты: ${}
                \n {} ({}) -> {} ₽ 
                """


weather = """
Погода в Оренбурге: {}°C,
Ощущается как: {}°C,
Приятного дня!
        """

history = '{date}: {crypto_value}({crypto_name}) -> {crypto_result} Р\n'


def remember_answer():
    list_message = ['Если не забуду, дам знать', 'Жди и надейся', 'Постараюсь напомнить вовремя',
                    'Если это так важно, то и напоминать не надо']
    random_answer = random.choice(list_message)
    return random_answer


fuck_off = """
Да пошли вы все
        """


def what_i_can(user_id):
        answer = """
Я умею:
показывать погоду;
Напоминать;
посылать всех;
выбрать жертву
        """
        if user_id == config.ADMIN_ID:
                answer = answer + '\nджарвис+=(погод, напомни, пошли всех, пошли их, выбери жертву), время сервера'
        return answer


budget_history = """
Категория: {},
На что: {},
Сумма: {} ₽
        """


help_message = '''
Бот работает в двух режимах:
1) в переписке с самим ботом; 
доступна работа с криптовалютой
можно узнать погоду города Оренбурга

2) при добавлении в чат, группу, можно писать боту, как ассистенту
его возможности можно узнать, написав:
'джарвис, что ты умеешь?'
'''


Messages = {'start': start_message, 'rates': rates, 'convert_result': convert_result,
            'weather': weather, 'history': history, 'fuck_off': fuck_off, 
            'budget_history': budget_history, 'help_message': help_message}
