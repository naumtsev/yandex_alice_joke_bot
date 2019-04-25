import requests
import json


def get_data(status):
    '1 - Анекдот 2 - Рассказы 3 - Стишки 4 - Афоризмы 5 - Цитаты 6 - Тост'
    URL = "http://rzhunemogu.ru/RandJSON.aspx?CType={}".format(status)
    data = requests.get(URL).text.replace('{"content":"', '').replace('"}', '')
    return data