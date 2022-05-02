import telegram
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import asyncio
from telegram.ext import CommandHandler
import random
import requests
import hashlib
from funcForWorkWithDB import getInformVK, TGid, getInformTG
from VKbot import waiting
from VK import VKToken, TGToken, GIF_api
import telebot
import discord
from discord.ext import commands
from discord_token import TOKEN
from discordBot import DiscordBot, BotsCog
import threading
from threading import Thread
import messagesFile
from io import BytesIO
from vk_api.upload import VkUpload



registrating = {}


vk_session = vk_api.VkApi(token=VKToken)
bot = telebot.TeleBot(TGToken)


async def TG_bot():
    longpoll = VkBotLongPoll(vk_session, "198062715")

    '''
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
    
    '''

    #thread1 = Thread(target=lambda: tgwaiting(updater))
    #thread2 = Thread(target=lambda: waiting(longpoll, vk_session, bot))

    #thread1.start()
    #thread2.start()

    Thread(target=tgwaiting, daemon=True).start()
    ##wrapper(longpoll, vk_session, bot)
    Thread(target=wrapper, args=(longpoll, vk_session, bot), daemon=True).start()
    ##await waiting(longpoll, vk_session, bot)

    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #asyncio.run_coroutine_threadsafe(waiting(longpoll, vk_session, bot), loop)


    #await asyncio.gather(
    #    asyncio.to_thread(tgwaiting, updater),
    #    asyncio.to_thread(waiting, longpoll, vk_session, bot),
    #    asyncio.sleep(1)
    #)
    print("okлллл")
    #updater.idle()
    #await
    #await


def wrapper(longpoll, vk_session, bot):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(waiting(longpoll, vk_session, bot))
    loop.close()


######################################################

#                      TELEGRAM                      #

######################################################

def tgwaiting():
    bot.polling(none_stop=True, interval=0)


@bot.message_handler(commands=['connect'])
def con(message):
    print("command connect")
    if message.chat.type == "private" and message.chat.id not in registrating.keys():
        try:
            req = getInformTG(message.from_user.id)
            print(message.from_user.id)
            print(req)
            bot.send_message(message.chat.id, f"Нет, {req[0][1]}, вы уже зарегистрированы")
        except Exception as e:
            print(e)
            registrating[message.chat.id] = ["id"]
            bot.send_message(message.chat.id, "Введите ваш VKid. Его вы можете получить в личных сообщениях нашего VK бота написав 'хочу узнать id'")
    else:
        bot.send_message(message.chat.id, "Осуществить привязку можно только в личных сообщениях t.me/CallMe_SanyaBot")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.id not in registrating.keys():
        print("not in keys")
        vk = vk_session.get_api()
        upload = VkUpload(vk)
        textt = message.text.lower()

        if message.chat.id == -400828697:
            try:
                req = getInformTG(message.from_user.id)
                print(req[0][1])
                # await disc.send_in_chat(event.obj.message['text'], req[0][1])
                messagesFile.discord_messages.append((message.text, req[0][1]))
                vk.messages.send(peer_id=2000000002,
                                 message=f"""{req[0][1]}:
                                                 {message.text}""",
                                 random_id=random.randint(0, 2 ** 64))
            except Exception as e:
                print(e)

                vk.messages.send(peer_id=2000000002,
                             message=f"""{message.from_user.username}:
                                 {message.text}""",
                             random_id=random.randint(0, 2 ** 64))
                messagesFile.discord_messages.append((message.text, message.from_user.username))
        if textt[:10] == "хочу гифку":
            textt = textt.replace("хочу гифку", "")
            endpoint = "https://g.tenor.com/v1/random"
            query_params = {"key": GIF_api}
            if textt.strip() != "":
                textt = textt.strip()
                query_params["q"] = textt

            response = requests.get(endpoint, params=query_params).json()
            print(response)
            bot.send_video(-400828697, response["results"][0]["media"][0]["gif"]["url"])
        if ("котик" in textt) or ("котейка" in textt):
            imgURL = requests.get("https://aws.random.cat/meow")
            print(imgURL)
            data = imgURL.text
            print(data)
            print("REAGY")
            img = requests.get(imgURL.json()["file"]).content
            bot.send_message(message.chat.id, 'Кто-то сказал "котик"?')
            bot.send_photo(message.chat.id, img)
            if message.chat.id == -400828697:
                f = BytesIO(img)

                photo = upload.photo_messages(f)[0]

                owner_id = photo['owner_id']
                photo_id = photo['id']
                access_key = photo['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(
                    random_id=random.randint(0, 2 ** 64),
                    peer_id=2000000002,
                    message='Кто-то сказал "котик"?'
                )
                vk.messages.send(
                    random_id=random.randint(0, 2 ** 64),
                    peer_id=2000000002,
                    attachment=attachment
                )
    else:
        print("in keys")
        if registrating[message.chat.id][0] == "id":
            try:
                res = getInformVK(message.text)
                print(res[0][0])
                bot.send_message(message.chat.id, "Хорошо! Теперь введите пароль, заданный при регистрации в VK")
                registrating[message.chat.id].append(message.text)
                registrating[message.chat.id][0] = "password"
            except Exception as e:
                bot.send_message(message.chat.id,
                                    "Произошло ошибка! Такого id не найдено, проверьте введённые данные.")
        elif registrating[message.chat.id][0] == "password":
            res = getInformVK(registrating[message.chat.id][1])
            password = hashlib.md5(bytes(message.text, encoding='utf8'))
            p = password.hexdigest()
            if res[0][2] == str(p):
                bot.send_message(message.chat.id, "Привязка прошла успешно! Спасибо что выбрали нашего бота!")
                TGid(message.from_user.id, registrating[message.chat.id][1])
            else:
                bot.send_message(message.chat.id, "Пароль не верен, проверьте введённые данные.")



'''


def echo(update, context):
    vk = vk_session.get_api()
    update.message.reply_text("Здравствуйте, " + update.message.from_user.username)
    update.message.reply_text("Я получил сообщение <" + update.message.text + ">")
    vk.messages.send(chat_id=2,
                     message=f"""{update.message.from_user.username}:
                     {update.message.text}""",
                     random_id=random.randint(0, 2 ** 64))
    messagesFile.vk_messages.append((update.message.text, update.message.from_user.username))


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


'''

#################################################

#                    MAIN                       #

#################################################

#async def disc_start(bot):
#    bot.run(TOKEN)

#if __name__ == '__main__':
#    bot = DiscordBot(command_prefix='!')
#    bot.add_cog(BotsCog(bot))
#    t1 = threading.Thread(target=VKandTG, args=(bot,))
#    t2 = threading.Thread(target=disc_start, args=(bot,))
#    t1.start()
#    t2.start()