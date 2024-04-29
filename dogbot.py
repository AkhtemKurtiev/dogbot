import os
from dotenv import load_dotenv

import requests
import logging

from telebot import TeleBot, types

load_dotenv()

bot = TeleBot(token=os.getenv('TOKEN'))

URL = 'http://shibe.online/api/shibes?count=1'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_new_image():
    try:
        response = requests.get(URL).json()
        random_dog = response[0]
        return random_dog
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url).json()
        return response[0].get('url')


@bot.message_handler(commands=['newdog'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    
    if not name:
        name = 'пользователь'
        
    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}.',
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_newdog = types.KeyboardButton('/newdog')
    keyboard.add(button_newdog)

    bot.send_message(
        chat.id,
        text=f'Привет, {name}. Фотография собаки',
        reply_markup=keyboard,
    )

    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я DogBot!')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
