# Для API
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# other
from Messages import Messages
import config
import time
import pickle

class MainParser:
    def usd_price():
        try:
            response = Session().get('https://www.cbr-xml-daily.ru/latest.js')
            data = json.loads(response.text)
            price = 1/data['rates']['USD']
        except:
            price = 0
        return round(price, 2)

    def cryptocurrency(name: str):
        cryptocurrencys = {'xrp': '52', 'btc': '1', 'eth': '1027'}
        crypto_id = cryptocurrencys[name]

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': config.CRYPTO_API_KEY,
        }
        parameters = {'id': crypto_id}

        try:
            response = Session().get(url, params=parameters, headers=headers)
            data = json.loads(response.text)
            price = data['data'][crypto_id]["quote"]['USD']['price']
        except:
            price = 0
        return round(price, 2)

    def cryptorates():
        cryptocurrencys = ['xrp', 'btc', 'eth']
        text = Messages['rates'].format(MainParser.cryptocurrency('btc'), 
                                        MainParser.cryptocurrency('xrp'), 
                                        MainParser.cryptocurrency('eth'), 
                                        MainParser.usd_price())

        return text

    def osnova(user_id, crypto_name, value):
        usd_price = MainParser.usd_price()
        price_crypto = MainParser.cryptocurrency(crypto_name)

        Result = round((float(price_crypto) * float(usd_price) * float(value)), 1)

        text = Messages['convert_result'].format(price_crypto, value, crypto_name, Result)

        # save in pickle
        time_now = str(time.strftime("%d.%m.%y", time.localtime()))
        values = [[time_now, crypto_name, value, price_crypto, Result, user_id]]

        with open('{}.data'.format(user_id), 'wb') as f:
            pickle.dump(values, f)

        return text
