import requests
import telebot
from telebot import types
import time
import threading

bot = telebot.TeleBot('7060286846:AAEeodWAegv3834hYLeNN_wsHjpFDWpxfY4')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! 👋 \nI can check the gate of a website. Please wait 10 seconds.')

    def countdown():
        time.sleep(10)
        bot.send_message(message.chat.id, 'You can now use the /url command.')

    thread = threading.Thread(target=countdown)
    thread.start()

@bot.message_handler(commands=['register'])
def register(message):
    user_id = message.from_user.id
    with open('database.txt', 'a') as file:
        file.write(str(user_id) + '\n')
    bot.send_message(message.chat.id, 'You have successfully registered! You can now use the /url command.')

@bot.message_handler(commands=['url'])
def url(message):
    user_id = message.from_user.id
    with open('database.txt', 'r') as file:
        registered_users = file.readlines()
        registered_users = [int(user.strip()) for user in registered_users]

    if user_id in registered_users:
        urls = message.text.split()[1:]
        if urls:
            bot.send_message(message.chat.id, 'Please wait, I\'m checking your URLs.')  # Added waiting message

            for url in urls:
                response = requests.get(f'http://157.10.53.104:8000/?url={url}')
                if response.status_code == 200:
                    data = response.json()
                    result = f'✿ Website » {data["site"]}\n\n'
                    result += f'✿ Captcha » {data["captcha"]}\n\n'
                    result += f'✿ Cloudflare » {data["cloudflare"]}\n\n'
                    result += f'✿ Gate » {", ".join(data["gate"])}'
                    bot.send_message(message.chat.id, result)
                else:
                    bot.send_message(message.chat.id, f'Error fetching data for: {url}')
        else:
            bot.send_message(message.chat.id, 'Please use the command in the following format: /url <website_url>')
    else:
        bot.send_message(message.chat.id, 'You need to register first! Use the /register command.')

bot.polling()
