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
from fileForWorkingWithDB import getInformVK, TGid, getInformTG
from VKbot import waiting
from VK import Nasa_api, GIF_api, IAM_TOKEN, TGToken, VKToken
import telebot
import discord
from discord.ext import commands
from discord_token import TOKEN
import datetime
from datetime import timedelta
import threading
from threading import Thread
import messagesFile
from io import BytesIO
from vk_api.upload import VkUpload
import wikipedia
from translate import Translator


registrating = {}


vk_session = vk_api.VkApi(token=VKToken)
bot = telebot.TeleBot(TGToken)


async def TG_bot():
    longpoll = VkBotLongPoll(vk_session, "198062715")

    Thread(target=tgwaiting, daemon=True).start()
    Thread(target=wrapper, args=(longpoll, vk_session, bot), daemon=True).start()
    print("okлллл")


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
    global bot
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
        elif ("котик" in textt) or ("котейка" in textt):
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
        elif textt == 'время':
            now = datetime.datetime.now()
            krat = timedelta(hours=3)
            if message.chat.id == -400828697:
                vk.messages.send(peer_id=2000000002,
                                 message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                 random_id=random.randint(0, 2 ** 64))
            bot.send_message(-400828697, (now + krat).strftime('%d/%m/%Y, %H:%M, %A'))
        elif textt[:4] == "вики":
            try:
                if message.chat.id == -400828697:
                    vk.messages.send(peer_id=2000000002,
                                     message=wikipedia.summary(textt[5:]),
                                     random_id=random.randint(0, 2 ** 64))
                bot.send_message(-400828697, wikipedia.summary(textt[5:]))
            except Exception as e:
                print(e)
                if message.chat.id == -400828697:
                    vk.messages.send(peer_id=2000000002,
                                     message="Ошибка!!!",
                                     random_id=random.randint(0, 2 ** 64))
                bot.send_message(-400828697, "Ошибка!!!")
        elif textt[:3] == "мем":
            temp = textt.replace("мем ", '')

            top = ''
            bot = ''

            temp = temp.split(', ')

            mem = temp[0]
            top = temp[1]
            bot = temp[2]

            print(temp)

            memes = {'1': '10-Guy', '2': '1990s-First-World-Problems',
                     '3': 'Aaaaand-Its-Gone', '4': '2nd-Term-Obama', '5': 'Advice-Doge',
                     '6': 'Albert-Einstein-1', '7': 'Am-I-The-Only-One-Around-Here'}

            if mem in memes.keys():
                querystring = {"top": top, "bottom": bot, "meme": memes[mem]}
                endpoint = "https://apimeme.com/meme"

                img = requests.get(endpoint, params=querystring).content
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
                        attachment=attachment
                    )
                bot.send_photo(-400828697, img)
            else:
                querystring = {"top": 'Ошибка!', "bottom": 'Указанный мем не найден!!!', "meme": 'FFFFFFFUUUUUUUUUUUU'}
                endpoint = "https://apimeme.com/meme"

                img = requests.get(endpoint, params=querystring).content
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
                        attachment=attachment
                    )
                bot.send_photo(-400828697, img)
        elif "фото" == textt:
            endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

            print("TRACK")
            query_params = {"api_key": Nasa_api, "earth_date": datetime.date.today().strftime("%y-%m-%d")}
            print(type(datetime.date.today().strftime("%y-%m-%d")))
            response = requests.get(endpoint, params=query_params)
            photos = response.json()["photos"]
            print("NEXT TRACK")
            for i in range(len(photos)):
                print(i)
                img = requests.get(photos[i]["img_src"]).content
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
                        attachment=attachment
                    )
                bot.send_photo(-400828697, img)
            print("Ended")
        elif "фото стандарт" == textt:
            endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

            print("TRACK")
            query_params = {"api_key": Nasa_api, "earth_date": "2020-07-01"}
            response = requests.get(endpoint, params=query_params)
            photos = response.json()["photos"]
            print("NEXT TRACK")
            for i in range(len(photos)):
                print(i)
                img = requests.get(photos[i]["img_src"]).content
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
                        attachment=attachment
                    )
                bot.send_photo(-400828697, img)
            print("Ended")
        elif textt == "космофото дня":
            response = requests.get("https://api.nasa.gov/planetary/apod?api_key=" + Nasa_api)
            print(response.content)
            img = requests.get(response.json()["url"]).content
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
                    attachment=attachment,
                    message=response.json()["title"] + '\n' + '\n' + response.json()["explanation"]
                )
            bot.send_photo(-400828697, img)
        elif textt == "интересность о числе":
            response = requests.get("http://numbersapi.com/random/")
            print(response.text)

            translator = Translator(to_lang="ru")

            translation = translator.translate(response.text)
            if message.chat.id == -400828697:
                vk.messages.send(
                    random_id=random.randint(0, 2 ** 64),
                    peer_id=2000000002,
                    message=translation
                )
            bot.send_message(-400828697, translation)

        elif textt[:20] == "интересность о числе":
            textt = textt.replace("интересность о числе ", '')
            try:
                temp = int(textt)
                print("http://numbersapi.com/" + textt.strip())
                response = requests.get("http://numbersapi.com/" + textt.strip())
                print(response.text)

                translator = Translator(to_lang="ru")

                translation = translator.translate(response.text)
                if message.chat.id == -400828697:
                    vk.messages.send(
                        random_id=random.randint(0, 2 ** 64),
                        peer_id=2000000002,
                        message=translation
                    )
                bot.send_message(-400828697, translation)
            except Exception as e:
                bot.send_message(-400828697, e)
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
                                    "Произошла ошибка! Такого id не найдено, проверьте введённые данные.")
        elif registrating[message.chat.id][0] == "password":
            res = getInformVK(registrating[message.chat.id][1])
            password = hashlib.md5(bytes(message.text, encoding='utf8'))
            p = password.hexdigest()
            if res[0][2] == str(p):
                bot.send_message(message.chat.id, "Привязка прошла успешно! Спасибо что выбрали нашего бота!")
                TGid(message.from_user.id, registrating[message.chat.id][1])
            else:
                bot.send_message(message.chat.id, "Пароль не верен, проверьте введённые данные.")
