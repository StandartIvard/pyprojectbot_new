import discord
from discord.ext import commands
import requests
import fileForWorkingWithDB
from discord_token import TOKEN
from VKbot import waiting
from vk_api.upload import VkUpload
import hashlib
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from VK import VKToken, TGToken
from main import TG_bot
import random
import asyncio
import messagesFile
from io import BytesIO
from PIL import Image
import datetime
from datetime import timedelta
import wikipedia
from main import TGbot

messagesFile.init()

vk_session = vk_api.VkApi(token=VKToken)
longpoll = VkBotLongPoll(vk_session, "198062715")


class BotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('What???')

    @commands.command(name='give_id')
    async def give_id(self, ctx):
        await bot.give_id(ctx)

    @commands.command(name='info')
    async def info(self, ctx):
        await bot.info(ctx)

    @commands.command(name='привязать')
    async def merge(self, ctx):
        pass

    @commands.command(name='время')
    async def time(self, ctx):
        await bot.send_time(ctx)

    @commands.command(name='вики')
    async def wiki(self, ctx, text):
        await bot.wiki(ctx, text)

    @commands.command(name='мем')
    async def meme(self, ctx, *text):
        await bot.meme(ctx, *text)

class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.users_list = {}
        self.last_author = ''
        super().__init__(*args, **kwargs)
        self.new_users = {}

    async def give_id(self, ctx):
        for member in bot.users_list.keys():
            if str(member) == ' '.join(ctx.message.content.split()[1:]):
                target = member
        try:
            await ctx.send(str(target.id))
        except Exception:
            await ctx.send('Пользователь не найден(')
        try:
            if ctx.channel.name != self.crosschat.name:
                raise Exception
            self.vk.messages.send(chat_id=2,
                                 message=f"""{str(target.id)}""",
                                 random_id=random.randint(0, 2 ** 64))
        except Exception:
            self.vk.messages.send(chat_id=2,
                                 message="Пользователь не найден(",
                                 random_id=random.randint(0, 2 ** 64))

    async def info(self, ctx):
        mes = 'Список команд:\n!give_id <имя пользователя> - id пользователя\n' \
              '!repeate <текст> - повторить текст\nСкоро команд будет больше.'
        await ctx.send(mes)
        try:
            if ctx.channel.name != self.crosschat.name:
                raise Exception
            self.vk.messages.send(chat_id=2,
                                 message=f"""{mes}""",
                                 random_id=random.randint(0, 2 ** 64))
        except Exception:
            pass

    async def send_time(self, ctx):
        now = datetime.datetime.now()
        krat = timedelta(hours=3)
        await ctx.send(str((now + krat).strftime('%d/%m/%Y, %H:%M, %A')))
        try:
            if ctx.channel.name != self.crosschat.name:
                raise Exception
            self.vk.messages.send(chat_id=2,
                                 message=f"""{str((now + krat).strftime('%d/%m/%Y, %H:%M, %A'))}""",
                                 random_id=random.randint(0, 2 ** 64))
        except Exception:
            pass

    async def wiki(self, ctx, text):
        try:
            await ctx.send(wikipedia.summary(text))
        except Exception:
            await ctx.send('Ошибка(')
        try:
            if ctx.channel.name != self.crosschat.name:
                raise Exception
            self.vk.messages.send(chat_id=2,
                                 message=f"""{wikipedia.summary(text)}""",
                                 random_id=random.randint(0, 2 ** 64))
        except Exception:
            pass

    async def meme(self, ctx, *text):

        tt = ' '.join(text)
        temp = tt.split(', ')
        mem = temp[0]
        top = temp[1]
        bot = temp[2]

        memes = {'1': '10-Guy',
                 '2': '1990s-First-World-Problems',
                 '3': 'Aaaaand-Its-Gone',
                 '4': '2nd-Term-Obama',
                 '5': 'Advice-Doge',
                 '6': 'Albert-Einstein-1',
                 '7': 'Am-I-The-Only-One-Around-Here'}
        if mem in list(memes.keys()):
            print('here')
            querystring = {"top": top, "bottom": bot, "meme": memes[mem]}
            endpoint = "https://apimeme.com/meme"

            img = requests.get(endpoint, params=querystring).content
            with open('new_p.png', 'wb') as new_p:
                new_p.write(img)
                await ctx.send(file=discord.File('new_p.png'))
                f = BytesIO(img)

                photo = self.upload.photo_messages(f)[0]

                owner_id = photo['owner_id']
                photo_id = photo['id']
                access_key = photo['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                self.vk.messages.send(
                random_id=random.randint(0, 2 ** 64),
                peer_id=2000000002,
                attachment=attachment
                )

    async def send_on_timer(self, channel_name, messages_list):
        await asyncio.sleep(0.01)
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel_name == channel.name:
                    cur_id = channel.id
        if len(messages_list) > 0:
            try:
                with open('new_p.png', 'wb') as new_p:
                    new_p.write(messages_list[0][2])
                await self.get_channel(cur_id).send(file=discord.File('new_p.png'))
            except Exception:
                await self.get_channel(cur_id).send('(' + messages_list[0][1] + '): ' + messages_list[0][0])
            messages_list.pop(0)
        self.loop.create_task(self.send_on_timer(channel_name, messages_list))

    async def on_ready(self):
        self.vk = vk_session.get_api()
        self.upload = VkUpload(self.vk)
        for g in self.guilds:
            for c in g.text_channels:
                await c.send('here i am')
            for m in g.members:
                if m.name not in self.users_list:
                    self.users_list[m] = 0
        for guild in self.guilds:
            for chat in guild.text_channels:
                if chat.name == 'bot_talking':
                    self.crosschat = chat
        await TG_bot(self)

    async def on_message(self, mes):
        if mes.author == self.user:
            return
        if mes.author not in self.users_list:
            self.users_list[mes.author] = 0
        self.users_list[mes.author] += 1
        try:
            try:
                if mes.channel.name == 'bot_talking':
                    for att in mes.attachments:
                        temp = att
                        await temp.save("""new_p.png""")
                    with open('new_p.png', 'rb') as new_p:
                        img = new_p.read()
                    f = BytesIO(img)
                    photo = self.upload.photo_messages(f)[0]
                    owner_id = photo['owner_id']
                    photo_id = photo['id']
                    access_key = photo['access_key']
                    attachments = f'photo{owner_id}_{photo_id}_{access_key}'
                    self.vk.messages.send(chat_id=2,
                                              message=f"""{str(mes.author)}:
                                              {str(mes.content)}""",
                                              random_id=random.randint(0, 2 ** 64),
                                              attachment=attachments)
                    TGbot.send_message(-400828697, str(mes.author) + ": " + str(mes.content))
            except Exception:
                if mes.channel.name == 'bot_talking':
                    self.vk.messages.send(chat_id=2,
                                          message=f"""{str(mes.author)}:
                                                      {str(mes.content)}""",
                                          random_id=random.randint(0, 2 ** 64),)
                    TGbot.send_message(-400828697, str(mes.author) + ": " + str(mes.content))
            if mes.content.startswith('!'):
                await self.process_commands(mes)
            self.last_author = mes.author
            if mes.channel.name != 'bot_talking':
                return
        except AttributeError:
            if mes.content.startswith('!привязать'):
                await mes.channel.send('Напишите ваш VK ID.')
                self.new_users[mes.author.id] = -1
            elif mes.author.id in self.new_users and self.new_users[mes.author.id] == -1:
                try:
                    self.new_users[mes.author.id] = int(mes.content.split()[0])
                    await mes.channel.send('Введите пароль, который вы получили у ботов других соц. сетей. Если вы потеряли пароль, напишите ... чтобы мы вам его напомнили.')
                except Exception:
                    await mes.channel.send('Что-то пошло не так, возможно вы ввели лишние символы или ещё как-то ошиблись в форме.')
            elif mes.author.id in self.new_users and self.new_users[mes.author.id] != -1:
                cur_users_data = fileForWorkingWithDB.getInformVK(self.new_users[mes.author.id])
                password = hashlib.md5(bytes(mes.content, encoding='utf8'))
                p = password.hexdigest()
                if cur_users_data[0][2] == str(p):
                    await mes.channel.send('Ура! Это вы - ' + fileForWorkingWithDB.getInformVK(self.new_users[mes.author.id])[0][1] + '?')
                    fileForWorkingWithDB.SetDiscord(cur_users_data[0][1], str(mes.author.id))
                else:
                    await mes.channel.send('Неверный пароль!')

    async def on_member_join(self, member):
        print(member)

    async def send_in_chat(self, text, author):
        await self.crosschat.send('(' + author + '): ' + text)

    def invite(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == 'общий':
                    return str(channel.create_invite())

    async def send_photo(self, url):
        img = requests.get(url).content
        with open('new_p.png', 'wb') as new_p:
            new_p.write(img)
            await self.crosschat.send(file=discord.File('new_p.png'))


bot = DiscordBot(command_prefix='!')
bot.add_cog(BotsCog(bot))

bot.loop.create_task(bot.send_on_timer('bot_talking', messagesFile.discord_messages))

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run(TOKEN))
loop.close()