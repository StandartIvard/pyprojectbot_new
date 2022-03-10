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
    update.message.reply_text(update.message.text)


async def main():
    vk_session = vk_api.VkApi(
        token="78fbb4ff6c6e02e47912a03f740b9057aebd0c553065f88da0d62645a1f33dc7ad37a6751446d5038c296")

    longpoll = VkBotLongPoll(vk_session, "198062715")


    updater = Updater("5153379485:AAHsOGBUilYA9gkwCfClzswlVc4BQeDhipo", use_context=True)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(text_handler)
    await asyncio.gather(updater.start_polling(), waiting(longpoll, vk_session))

    updater.idle()


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
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="ок",
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