import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
from datetime import timedelta
from funcForWorkWithDB import insertVK, VKpass, getInformVK
import asyncio

import telegram

regid = list()


async def waiting(longpoll, vk_session, disc):
    scen = 0

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
                if ("регистрация" in textt):
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

                        regid.append(event.obj.message['from_id'])

                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text and event.obj.message['from_id'] in regid:
                                insertVK(event.obj.message['text'], str(event.obj.message['from_id']))

                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message="Хорошо, " + event.obj.message['text'] + ", придумайте пароль.",
                                                 random_id=random.randint(0, 2 ** 64))

                                for event in longpoll.listen():
                                    if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
                                        VKpass(event.obj.message['text'], event.obj.message['from_id'])
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message='''Регистрация завершена!
                                                                Вы также можете привязать свой аккаунт в Discord. 
                                                                Для этого напишите "привязать дискорд".
                                                                Кроме этого вы можете привязать Telegram, однако эта привязка не осуществляется через Vk.
                                                                Для получения дальнейших инструкций вы можете написать t.me/CallMe_SanyaBot.
                                                                Приятного пользования!''',
                                                         random_id=random.randint(0, 2 ** 64))
                                        break
                                break

                elif textt == "привязки":
                    vk.messages.send(user_id=event.obj.message['from_id'],
                        message='''Вы можете привязать свой аккаунт в Discord. 
                        Для этого напишите "привязать дискорд".
                        Кроме этого вы можете привязать Telegram, однако эта привязка не осуществляется через Vk.
                        Для получения дальнейших инструкций вы можете написать t.me/CallMe_SanyaBot.
                        Приятного пользования!''',
                                     random_id=random.randint(0, 2 ** 64))

                elif (("день" in textt) or ("время" in textt) or\
                        ("дата" in textt) or ("число" in textt)):
                    now = datetime.datetime.now()
                    krat = timedelta(hours=3)

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                     random_id=random.randint(0, 2 ** 64))

                elif textt == "хочу узнать id" and scen == 0:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Ваш id в VK - " + str(event.obj.message['from_id']),
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
                    elif textt == "кто я":
                        try:
                            req = getInformVK(event.obj.message['from_id'])
                            print(req)
                            vk.messages.send(chat_id=event.chat_id,
                                             message=f"""Это {req[0][1]}""",
                                             random_id=random.randint(0, 2 ** 64))
                        except Exception:
                            user_get = vk.users.get(user_ids=(str(event.obj.message['from_id'])))
                            user_get = user_get[0]
                            first_name = user_get['first_name']
                            last_name = user_get['last_name']
                            full_name = first_name + " " + last_name
                            vk.messages.send(chat_id=event.chat_id,
                                             message=f"""Это {full_name}""",
                                             random_id=random.randint(0, 2 ** 64))
                    elif textt == "id беседы":
                        vk.messages.send(chat_id=event.chat_id,
                                         message="id этой беседы - " + str(event.chat_id),
                                         random_id=random.randint(0, 2 ** 64))
                        print(str(event.chat_id))

                if event.chat_id == 2:
                    try:
                        req = getInformVK(event.obj.message['from_id'])
                        print(req[0][1])
                        await disc.send_in_chat(event.obj.message['text'], req[0][1])
                    except Exception as e:
                        print(e)
                        user_get = vk.users.get(user_ids=(str(event.obj.message['from_id'])))
                        user_get = user_get[0]
                        first_name = user_get['first_name']
                        last_name = user_get['last_name']
                        full_name = first_name + " " + last_name
                        await disc.send_in_chat(event.obj.message['text'], full_name)
