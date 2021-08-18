import requests
import asyncio
import time
from requests import Session
from Messages import Messages
import config


def Orenburg():
    url = 'https://api.openweathermap.org/data/2.5/weather'    
    params = {'units': 'metric', 'id': '515003', 'APPID': config.WEATHER_KEY}   
    res = Session().get(url, params=params)
    try:
        api_result = res.json()
        tempr = res.json()['main']['temp']
        feels_like = res.json()['main']['feels_like']
        return {'tempr': tempr, 'feels_like': feels_like}
    except:
        return False

def weather_messages():
    weather_result = Orenburg()
    if weather_result:
        return Messages['weather'].format(weather_result['tempr'], weather_result['feels_like'])
    else:
        return False
