import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
from datetime import timedelta
from funcForWorkWithDB import insertVK, VKpass


async def waiting(longpoll, vk_session):
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
                if ("регистрация" in textt) and scen == 0:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Введите желаемое имя",
                                     random_id=random.randint(0, 2 ** 64))
                    scen = 1

                elif scen == 1:
                    insertVK(event.obj.message['text'], str(event.obj.message['from_id']))
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Хорошо, " + event.obj.message['text'] + ", придумайте пароль.",
                                     random_id=random.randint(0, 2 ** 64))
                    scen = 2

                elif scen == 2:
                    VKpass(event.obj.message['text'], event.obj.message['from_id'])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                        message='''Регистрация завершена! Вы также можете привязать свои аккаунты в Discord и Telegram. 
                        Для этого напишите "привязать дискорд" или "привязать телегу" соответственно. 
                        Приятного пользования!''',
                                     random_id=random.randint(0, 2 ** 64))

                elif (("день" in textt) or ("время" in textt) or\
                        ("дата" in textt) or ("число" in textt)) and scen == 0:
                    now = datetime.datetime.now()
                    krat = timedelta(hours=3)

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=(now + krat).strftime('%d/%m/%Y, %H:%M, %A'),
                                     random_id=random.randint(0, 2 ** 64))

                elif textt == "хочу узнать id" and scen == 0:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Ваш vk id - " + str(event.obj.message['from_id']),
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