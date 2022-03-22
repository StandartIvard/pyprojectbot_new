import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import asyncio
from telegram.ext import CommandHandler
import hashlib
from VKbot import waiting


async def main():
    updater = Updater("5153379485:AAHsOGBUilYA9gkwCfClzswlVc4BQeDhipo", use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(text_handler)

    vk_session = vk_api.VkApi(token="78fbb4ff6c6e02e47912a03f740b9057aebd0c553065f88da0d62645a1f33dc7ad37a6751446d5038c296")
    longpoll = VkBotLongPoll(vk_session, "198062715")

    await asyncio.gather(tgwaiting(updater), waiting(longpoll, vk_session))

    updater.idle()


######################################################

#                      TELEGRAM                      #

######################################################


async def tgwaiting(updater):
    updater.start_polling()


def echo(update, context):
    update.message.reply_text("Здравствуйте, " + update.message.from_user.username)
    update.message.reply_text("Я получил сообщение <" + update.message.text + ">")


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


#################################################

#                    MAIN                       #

#################################################


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())