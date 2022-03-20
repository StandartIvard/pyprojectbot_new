import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
from datetime import timedelta
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import pytz
import asyncio
from telegram.ext import CommandHandler


def echo(update, context):
    update.message.reply_text("Я получил сообщение <" + update.message.text + ">")


async def main():
    vkreg = False
    updater = Updater("5153379485:AAHsOGBUilYA9gkwCfClzswlVc4BQeDhipo", use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(text_handler)

    vk_session = vk_api.VkApi(token="78fbb4ff6c6e02e47912a03f740b9057aebd0c553065f88da0d62645a1f33dc7ad37a6751446d5038c296")
    longpoll = VkBotLongPoll(vk_session, "198062715")

    print("ok")

    await asyncio.gather(tgwaiting(updater), waiting(longpoll, vk_session))

    updater.idle()

    print("ok")


async def waiting(longpoll, vk_session):

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            vk = vk_session.get_api()

            id = str(event.obj.message['from_id'])
            user_get = vk.users.get(user_ids=(id))
            user_get = user_get[0]
            first_name = user_get['first_name']
            last_name = user_get['last_name']
            full_name = first_name + " " + last_name
            print(full_name)

            textt = event.obj.message['text'].lower()
            if event.from_user:
                if ("день" in textt) or ("время" in textt) or\
                        ("дата" in textt) or ("число" in textt):
                    now = datetime.datetime.now()
                    krat = timedelta(hours=3)

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                     random_id=random.randint(0, 2 ** 64))
                if ("регистрация" in textt):
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Здравствуйте",
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="""Вы можете узнать текущую дату, время и день недели, 
                                     написав <<время>>, <<число>>, <<дата>> и <<день>>""",
                                     random_id=random.randint(0, 2 ** 64))
            elif event.from_chat:
                if textt[0] == '/':
                    textt = textt.replace('/', '')
                    if textt == 'время':
                        now = datetime.datetime.now()
                        krat = timedelta(hours=3)
                        vk.messages.send(chat_id=event.chat_id,
                                         message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                         random_id=random.randint(0, 2 ** 64))


async def tgwaiting(updater):
    updater.start_polling()


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


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