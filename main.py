import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
from datetime import timedelta
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import pytz
import asyncio


def echo(update, context):
    update.message.reply_text("Я получил сообщение <" + update.message.text + ">")


async def main():
    updater = Updater("5153379485:AAHsOGBUilYA9gkwCfClzswlVc4BQeDhipo", use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.idle()

    vk_session = vk_api.VkApi(
    token="78fbb4ff6c6e02e47912a03f740b9057aebd0c553065f88da0d62645a1f33dc7ad37a6751446d5038c296")
    longpoll = VkBotLongPoll(vk_session, "198062715")

    await asyncio.gather(updater.start_polling(), waiting(longpoll, vk_session))

    print("ok")


def waiting(longpoll, vk_session):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            if ("день" in event.obj.message['text']) or ("время" in event.obj.message['text']) or\
                    ("дата" in event.obj.message['text']) or ("число" in event.obj.message['text']):
                now = datetime.datetime.now()
                krat = timedelta(hours=3)
                vk = vk_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk = vk_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="""Вы можете узнать текущую дату, время и день недели, 
                                 написав <<время>>, <<число>>, <<дата>> и <<день>>""",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

'''
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


def main():
    login, password = "ivard_iv@mail.ru", "UMSAforever12345"
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if "доброе утро" in event.text.lower() and event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=event.random_id,
                    message='Ваш текст')


if __name__ == '__main__':
    main()
'''