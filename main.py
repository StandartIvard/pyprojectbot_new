import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import pytz


def main():
    vk_session = vk_api.VkApi(
        token="78fbb4ff6c6e02e47912a03f740b9057aebd0c553065f88da0d62645a1f33dc7ad37a6751446d5038c296")

    longpoll = VkBotLongPoll(vk_session, "198062715")

    for event in longpoll.listen():

        if datetime.datetime.now(pytz.timezone("KRAT")) == datetime.time(23, 20, 0):
            vk = vk_session.get_api()
            vk.messages.send(user_id="klownishe",
                             message=now.strftime('%d/%m/%Y, %H:%M, %A'),
                             random_id=random.randint(0, 2 ** 64))

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            if ("день" in event.obj.message['text']) or ("время" in event.obj.message['text']) or\
                    ("дата" in event.obj.message['text']) or ("число" in event.obj.message['text']):
                now = datetime.datetime.now()
                vk = vk_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=now.strftime('%d/%m/%Y, %H:%M, %A'),
                                 random_id=random.randint(0, 2 ** 64))
                print()
            else:
                vk = vk_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="""Вы можете узнать текущую дату, время и день недели, 
                                 написав <<время>>, <<число>>, <<дата>> и <<день>>""",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()