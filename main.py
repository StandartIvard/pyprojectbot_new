import telegram
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import asyncio
from telegram.ext import CommandHandler
import random
import hashlib
from VKbot import waiting
from VK import VKToken, TGToken
import discord
from discord.ext import commands
from discord_token import TOKEN
from discordBot import DiscordBot, BotsCog
import threading

vk_session = vk_api.VkApi(token=VKToken)


async def TG_bot(bot):
    longpoll = VkBotLongPoll(vk_session, "198062715")
    updater = Updater(TGToken, use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('vkConnect', vkConnect)],
        states={
            1: [MessageHandler(Filters.text, first)],
        },
        fallbacks = [CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("id", id))
    dp.add_handler(text_handler)

    await tgwaiting(updater)
    await waiting(longpoll, vk_session, bot)

    updater.idle()


######################################################

#                      TELEGRAM                      #

######################################################


async def tgwaiting(updater):
    updater.start_polling()


def echo(update, context):
    vk = vk_session.get_api()
    update.message.reply_text("Здравствуйте, " + update.message.from_user.username)
    update.message.reply_text("Я получил сообщение <" + update.message.text + ">")
    vk.messages.send(chat_id=2,
                     message=f"""{update.message.from_user.username}:
                     {update.message.text}""",
                     random_id=random.randint(0, 2 ** 64))


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def id(update, context):
    update.message.reply_text(
        f"Ваш id: {update.message.from_user.id}")

def stop(update, context):
    update.message.reply_text(
        "Ну ладно...")


def vkConnect(update, context):
    update.message.reply_text("""Чтобы начать привязку аккаунта Vk введите ваш id.
    Его вы можете узнать, написав боту вк 'хочу узнать id'.""")
    return 1


def first(update, context):
    vk = vk_session.get_api()
    vk.messages.send(user_id=int(update.message.text),
                     message="Чтобы подтвердить привязку аккаунта к Telegram, введите ваш пароль.",
                     random_id=random.randint(0, 2 ** 64))


#################################################

#                    MAIN                       #

#################################################

async def disc_start(bot):
    bot.run(TOKEN)

#if __name__ == '__main__':
#    bot = DiscordBot(command_prefix='!')
#    bot.add_cog(BotsCog(bot))
#    t1 = threading.Thread(target=VKandTG, args=(bot,))
#    t2 = threading.Thread(target=disc_start, args=(bot,))
#    t1.start()
#    t2.start()