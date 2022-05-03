import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
from datetime import timedelta
from fileForWorkingWithDB import insertVK, VKpass, getInformVK
from vk_api.upload import VkUpload
import asyncio
import wikipedia
import telegram
import requests
from io import BytesIO
from VK import Nasa_api, GIF_api, IAM_TOKEN, TGToken
import messagesFile
import json
from translate import Translator
import telebot

regid = {}
wikipedia.set_lang("ru")

members = []


async def waiting(longpoll, vk_session, tg_bot):
    scen = 0
    vk = vk_session.get_api()
    upload = VkUpload(vk)

    for event in longpoll.listen():
        print(event.type)
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            print(1)
            print(event.obj.message["attachments"])
            print(2)

            id = str(event.obj.message['from_id'])
            user_get = vk.users.get(user_ids=(id))
            user_get = user_get[0]
            first_name = user_get['first_name']
            last_name = user_get['last_name']
            full_name = first_name + " " + last_name
            print(full_name)

            textt = event.obj.message['text'].lower()
            if event.from_user:
                if "регистрация" in textt:
                    try:
                        req = getInformVK(event.obj.message['from_id'])
                        print(req)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                        message=f"""Нет, {req[0][1]}, вы уже зарегистрированы""",
                                        random_id=random.randint(0, 2 ** 64))
                    except Exception:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                        message="Введите желаемое имя",
                                        random_id=random.randint(0, 2 ** 64))
                        regid[event.obj.message['from_id']] = "name"

                elif event.obj.message['from_id'] in regid.keys():
                    if regid[event.obj.message['from_id']] == "name":
                        insertVK(event.obj.message['text'], str(event.obj.message['from_id']))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Хорошо, " + event.obj.message['text'] + ", придумайте пароль.",
                                         random_id=random.randint(0, 2 ** 64))
                        regid[event.obj.message['from_id']] = "password"

                    elif regid[event.obj.message['from_id']] == "password":
                        VKpass(event.obj.message['text'], event.obj.message['from_id'])
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='''Регистрация завершена!
                                                Вы также можете привязать свой аккаунт в Discord. 
                                                Для этого напишите "привязать дискорд".
                                                Кроме этого вы можете привязать Telegram, однако эта привязка не осуществляется через Vk.
                                                Для получения дальнейших инструкций вы можете написать t.me/CallMe_SanyaBot.
                                                Приятного пользования!''',
                                         random_id=random.randint(0, 2 ** 64))
                        del regid[event.obj.message['from_id']]

                elif textt == "привязки":
                    vk.messages.send(user_id=event.obj.message['from_id'],
                        message='''Вы можете привязать свой аккаунт в Discord. 
                        Для этого напишите "привязать дискорд".
                        Кроме этого вы можете привязать Telegram, однако эта привязка не осуществляется через Vk.
                        Для получения дальнейших инструкций вы можете написать t.me/CallMe_SanyaBot.
                        Приятного пользования!''',
                                     random_id=random.randint(0, 2 ** 64))

                    #await disc.send_in_chat(event.obj.message['text'], full_name)

                elif (("день" in textt) or ("время" in textt) or\
                        ("дата" in textt) or ("число" in textt)):
                    now = datetime.datetime.now()
                    krat = timedelta(hours=3)

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                     random_id=random.randint(0, 2 ** 64))

                elif textt == "хочу узнать id":
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Ваш id в VK - " + str(event.obj.message['from_id']),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.from_chat:
                if event.chat_id == 2:
                    try:
                        req = getInformVK(event.obj.message['from_id'])
                        print(req[0][1])
                        #await disc.send_in_chat(event.obj.message['text'], req[0][1])
                        if event.obj.message['text']:
                            messagesFile.discord_messages.append((event.obj.message['text'], req[0][1]))
                            tg_bot.send_message(-400828697, req[0][1] + ": " + event.obj.message['text'])
                        if len(event.obj.message["attachments"]) > 0:
                            if event.obj.message["attachments"][0]['type'] == "photo":
                                img = requests.get(event.obj.message["attachments"][0]['photo']['sizes'][-1]['url']).content
                                tg_bot.send_photo(-400828697, img)
                    except Exception as e:
                        print(e)
                        user_get = vk.users.get(user_ids=(str(event.obj.message['from_id'])))
                        user_get = user_get[0]
                        first_name = user_get['first_name']
                        last_name = user_get['last_name']
                        full_name = first_name + " " + last_name
                        #await disc.send_in_chat(event.obj.message['text'], full_name)
                        messagesFile.discord_messages.append((event.obj.message['text'], full_name))
                        tg_bot.send_message(-400828697, full_name + ": " + event.obj.message['text'])
                    members = vk.messages.getConversationMembers(
                        peer_id=event.obj.message["peer_id"],
                    )['items']
                    members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                    f = open("vk_users.txt")
                    temp = f.read()
                    temp = temp.split(" ")
                    temp[0] = temp[0].lstrip('\x00')
                    members_ids = list(map(str, members_ids))
                    if temp != members_ids:
                        print(temp)
                        print(members_ids)
                        for member_id in range(len(members_ids)):
                            if members_ids[member_id] not in temp:
                                message = f'[id{members_ids[member_id]}|Приветствуем тебя в нашей мультибеседе!]'
                                vk.messages.send(
                                    peer_id=2000000002,
                                    message=message,
                                    random_id=random.randint(0, 2 ** 64)
                                )
                        f.close()
                        f = open("vk_users.txt", "w")
                        f.seek(1)
                        temp = " ".join(members_ids)
                        f.write(temp)
                        f.close()

                if len(textt) > 0:
                    if textt[0] == '/':
                        textt = textt.replace('/', '')
                        if textt == 'время':
                            now = datetime.datetime.now()
                            krat = timedelta(hours=3)
                            vk.messages.send(chat_id=event.chat_id,
                                             message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                             random_id=random.randint(0, 2 ** 64))
                            if event.obj.message['peer_id'] == 2000000002:
                                tg_bot.send_message(-400828697, (now + krat).strftime('%d/%m/%Y, %H:%M, %A'))
                        elif textt == "кто я":
                            try:
                                req = getInformVK(event.obj.message['from_id'])
                                print(req)
                                vk.messages.send(chat_id=event.chat_id,
                                                 message=f"""Это {req[0][1]}""",
                                                 random_id=random.randint(0, 2 ** 64))
                                if event.obj.message['peer_id'] == 2000000002:
                                    tg_bot.send_message(-400828697, f"""Это {req[0][1]}""")
                            except Exception:
                                user_get = vk.users.get(user_ids=(str(event.obj.message['from_id'])))
                                user_get = user_get[0]
                                first_name = user_get['first_name']
                                last_name = user_get['last_name']
                                full_name = first_name + " " + last_name
                                vk.messages.send(chat_id=event.chat_id,
                                                 message=f"""Это {full_name}""",
                                                 random_id=random.randint(0, 2 ** 64))
                                if event.obj.message['peer_id'] == 2000000002:
                                    tg_bot.send_message(-400828697, f"""Это {full_name}""")
                        elif textt == "id беседы":
                            vk.messages.send(chat_id=event.chat_id,
                                             message="id этой беседы - " + str(event.chat_id),
                                             random_id=random.randint(0, 2 ** 64))
                            print(str(event.chat_id))
                        elif textt[:4] == "вики":
                            try:
                                vk.messages.send(chat_id=event.chat_id,
                                                 message=wikipedia.summary(textt[5:]),
                                                 random_id=random.randint(0, 2 ** 64))
                                if event.obj.message['peer_id'] == 2000000002:
                                    tg_bot.send_message(-400828697, wikipedia.summary(textt[5:]))
                            except Exception as e:
                                print(e)
                                vk.messages.send(chat_id=event.chat_id,
                                                 message="Ошибка!!!",
                                                 random_id=random.randint(0, 2 ** 64))
                                if event.obj.message['peer_id'] == 2000000002:
                                    tg_bot.send_message(-400828697, "Ошибка!!!")
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
                                f = BytesIO(img)

                                photo = upload.photo_messages(f)[0]

                                owner_id = photo['owner_id']
                                photo_id = photo['id']
                                access_key = photo['access_key']
                                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                                vk.messages.send(
                                    random_id=random.randint(0, 2 ** 64),
                                    peer_id=event.message.peer_id,
                                    attachment=attachment
                                )
                                if event.obj.message['peer_id'] == 2000000002:
                                    tg_bot.send_photo(-400828697, img)
                            else:
                                querystring = {"top": 'Ошибка!', "bottom": 'Указанный мем не найден!!!', "meme": 'FFFFFFFUUUUUUUUUUUU'}
                                endpoint = "https://apimeme.com/meme"

                                img = requests.get(endpoint, params=querystring).content
                                f = BytesIO(img)

                                photo = upload.photo_messages(f)[0]

                                owner_id = photo['owner_id']
                                photo_id = photo['id']
                                access_key = photo['access_key']
                                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                                vk.messages.send(
                                    random_id=random.randint(0, 2 ** 64),
                                    peer_id=event.message.peer_id,
                                    attachment=attachment
                                )
                                if event.obj.message['peer_id'] == 2000000002:
                                    tg_bot.send_photo(-400828697, img)

                if "фото" == textt:
                    endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

                    print("TRACK")
                    #query_params = {"api_key": Nasa_api, "earth_date": datetime.date.today().strftime("%y-%m-%d")}
                    query_params = {"api_key": Nasa_api, "earth_date": "2020-07-01"}
                    print(type(datetime.date.today().strftime("%y-%m-%d")))
                    response = requests.get(endpoint, params=query_params)
                    photos = response.json()["photos"]
                    print("NEXT TRACK")
                    for i in range(len(photos)):
                        print(i)
                        img = requests.get(photos[i]["img_src"]).content
                        f = BytesIO(img)

                        photo = upload.photo_messages(f)[0]

                        owner_id = photo['owner_id']
                        photo_id = photo['id']
                        access_key = photo['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(
                            random_id=random.randint(0, 2 ** 64),
                            peer_id=event.message.peer_id,
                            attachment=attachment
                        )
                        if event.obj.message['peer_id'] == 2000000002:
                            tg_bot.send_photo(-400828697, img)
                    print("Ended")

                if ("котик" in textt) or ("котейка" in textt):
                    imgURL = requests.get("https://aws.random.cat/meow")
                    data = imgURL.text
                    print(data)
                    print("REAGY")
                    img = requests.get(imgURL.json()["file"]).content
                    f = BytesIO(img)

                    photo = upload.photo_messages(f)[0]

                    owner_id = photo['owner_id']
                    photo_id = photo['id']
                    access_key = photo['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    vk.messages.send(
                        random_id=random.randint(0, 2 ** 64),
                        peer_id=event.message.peer_id,
                        message='Кто-то сказал "котик"?'
                    )
                    vk.messages.send(
                        random_id=random.randint(0, 2 ** 64),
                        peer_id=event.message.peer_id,
                        attachment=attachment
                    )
                    if event.obj.message['peer_id'] == 2000000002:
                        tg_bot.send_photo(-400828697, img)

                elif textt == "космофото дня":
                    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=" + Nasa_api)
                    print(response.content)
                    img = requests.get(response.json()["url"]).content
                    f = BytesIO(img)

                    photo = upload.photo_messages(f)[0]

                    owner_id = photo['owner_id']
                    photo_id = photo['id']
                    access_key = photo['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    vk.messages.send(
                        random_id=random.randint(0, 2 ** 64),
                        peer_id=event.message.peer_id,
                        attachment=attachment,
                        message=response.json()["title"] + '\n' + '\n' + response.json()["explanation"]
                    )
                    if event.obj.message['peer_id'] == 2000000002:
                        tg_bot.send_photo(-400828697, img)

                elif textt == "интересность о числе":
                    response = requests.get("http://numbersapi.com/random/")
                    print(response.text)

                    translator = Translator(to_lang="ru")

                    translation = translator.translate(response.text)

                    vk.messages.send(
                        random_id=random.randint(0, 2 ** 64),
                        peer_id=event.message.peer_id,
                        message=translation
                    )
                    if event.obj.message['peer_id'] == 2000000002:
                        tg_bot.send_message(-400828697, translation)

                elif textt[:20] == "интересность о числе":
                    textt = textt.replace("интересность о числе ", '')
                    try:
                        temp = int(textt)
                        print("http://numbersapi.com/" + textt.strip())
                        response = requests.get("http://numbersapi.com/" + textt.strip())
                        print(response.text)

                        translator = Translator(to_lang="ru")

                        translation = translator.translate(response.text)

                        vk.messages.send(
                            random_id=random.randint(0, 2 ** 64),
                            peer_id=event.message.peer_id,
                            message=translation
                        )
                        if event.obj.message['peer_id'] == 2000000002:
                            tg_bot.send_message(-400828697, translation)
                    except Exception as e:
                        vk.messages.send(
                            random_id=random.randint(0, 2 ** 64),
                            peer_id=event.message.peer_id,
                            message=e
                        )
