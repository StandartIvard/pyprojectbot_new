import discord
from discord.ext import commands
from discord_token import TOKEN
from VKbot import waiting
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from VK import VKToken, TGToken
from main import TG_bot
import random
import asyncio
import messagesFile

messagesFile.init()

vk_session = vk_api.VkApi(token=VKToken)
longpoll = VkBotLongPoll(vk_session, "198062715")


class BotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('What???')

    @commands.command(name='points')
    async def points(self, ctx):
        await ctx.send(ctx.message.author.mention + ' у тебя ' + str(bot.users_list[str(ctx.message.author)]) + ' очков!')

    @commands.command(name='repeate')
    async def repeate_fraze(self, ctx, *text):
        if str(bot.last_author) == str(ctx.message.author):
            for channel in ctx.guild.text_channels:
                if channel.name == 'bot_talking':
                    await channel.send('(' + str(ctx.author) + '): ' + ' '.join(text))

    @commands.command(name='give_id')
    async def give_id(self, ctx):
        for member in bot.users_list.keys():
            if str(member) == ' '.join(ctx.message.content.split()[1:]):
                target = member
        try:
            await ctx.send(str(target.id))
        except Exception:
            await ctx.send('Пользователь не найден(')

    @commands.command(name='info')
    async def info(self, ctx):
        await ctx.send('Список команд:\n!give_id <имя пользователя> - id пользователя\n'
                       '!repeate <текст> - повторить текст\nСкоро команд будет больше.')


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.users_list = {}
        self.last_author = ''
        super().__init__(*args, **kwargs)

    async def send_on_timer(self, channel_name, messages_list):
        await asyncio.sleep(0.01)
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel_name == channel.name:
                    cur_id = channel.id
        if len(messages_list) > 0:
            await self.get_channel(cur_id).send('(' + messages_list[0][1] + '): ' + messages_list[0][0])
            messages_list.pop(0)
        self.loop.create_task(self.send_on_timer(channel_name, messages_list))

    async def on_ready(self):
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
        if mes.content.startswith('!'):
            await self.process_commands(mes)
        self.last_author = mes.author
        if mes.channel.name != 'bot_talking':
            return
        vk = vk_session.get_api()
        vk.messages.send(chat_id=2,
                         message=f"""{str(mes.author)}:
                             {str(mes.content)}""",
                         random_id=random.randint(0, 2 ** 64))

    async def on_member_join(self, member):
        print(member)

    async def send_in_chat(self, text, author):
        await self.crosschat.send('(' + author + '): ' + text)

    def invite(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == 'общий':
                    return str(channel.create_invite())


bot = DiscordBot(command_prefix='!')
bot.add_cog(BotsCog(bot))
bot.loop.create_task(bot.send_on_timer('bot_talking', messagesFile.vk_messages))

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run(TOKEN))
loop.close()