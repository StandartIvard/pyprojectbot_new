from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import telebot
from VK import TGToken



TGbot = telebot.TeleBot(TGToken)


@TGbot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        TGbot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        TGbot.send_message(message.from_user.id, "Напиши привет")
    else:
        TGbot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


TGbot.polling(none_stop=True, interval=0)