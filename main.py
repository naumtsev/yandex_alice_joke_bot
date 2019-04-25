from flask import Flask, request
import json
# импортируем функции из нашего второго файла geo
from laughter import get_data
import random
import datetime
app = Flask(__name__)

Users = dict()

def get_seconds_by_start():
    return datetime.timestamp()

keywords = [('анекдот', 1), ('рассказ', 2), ('стих', 3), ('цитату', 5), ('тост', 6)]
go_next = ['давай я ещё что-нибудь тебе расскажу!', 'ты ещё не устал? Говорят, что смех даёт силу. Порекомендую тебе послушать анекдот!',
           'давай я тебе расскажу стих.', 'у меня есть пару цитат для тебя!', 'у меня появилися новый рассказ, может послушаешь?',
           'не хочешь посмеяться?', 'если вы находитесь за столом, самое время говорить тост!', 'кажется настало время для тоста!', 'у меня есть интересная шутейка!']

@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = \
            'Привет, я Алиса, мои возможности безграничны, но особенно хорошо я знаю и умею рассказывать: анекдоты, рассказы, стихотворения, цитаты, а так же тосты! ' \
            ' Мне неудобно разговаривать с тобой на "вы", как тебя зовут?'
        Users[user_id] = dict()
        Users[user_id]['name'] = None
        return

    if Users[user_id]['name'] is None:
        name = get_name(req)
        if name is None:
            res['response']['text'] = \
                'Я не расслышала твоё имя, повтори пожалуйста.'
            return
        name = name[0].upper() + name[1:].lower()

        Users[user_id]['name'] = name

        res['response']['text'] = \
            'Рада познакомиться с тобой, {}! Давай я что-нибудь тебе расскажу!'.format(name)
        res['response']['buttons'] = [
            {
                'title': 'Анекдот',
                'hide': True
            },
            {
                'title': 'Рассказ',
                'hide': True
            },
            {
                'title': 'Стих',
                'hide': True
            },
            {
                'title': 'Цитату',
                'hide': True
            },
            {
                'title': 'Тост',
                'hide': True
            },
        ]
        return

    words = req['request']['nlu']['tokens']
    for now_word, now_key in keywords:
        if now_word in words:
            text = get_data(now_key)
            res['response']['text'] = \
                '{}\n{}, {}'.format(text, Users[user_id]['name'], random.choice(go_next))
            res['response']['buttons'] = [
                {
                    'title': 'Анекдот',
                    'hide': True
                },
                {
                    'title': 'Рассказ',
                    'hide': True
                },
                {
                    'title': 'Стих',
                    'hide': True
                },
                {
                    'title': 'Цитату',
                    'hide': True
                },
                {
                    'title': 'Тост',
                    'hide': True
                },
            ]
            return

    res['response']['text'] = \
        'Прости я не совсем поняла, что ты хочешь услышать'
    res['response']['buttons'] = [
        {
            'title': 'Анекдот',
            'hide': True
        },
        {
            'title': 'Рассказ',
            'hide': True
        },
        {
            'title': 'Стих',
            'hide': True
        },
        {
            'title': 'Цитату',
            'hide': True
        },
        {
            'title': 'Тост',
            'hide': True
        },
    ]
    return



def get_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if ('first_name' in entity['value']):
                return entity['value']['first_name']
            return None


if __name__ == '__main__':
    app.run()