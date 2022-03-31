import discord
from discord.ext import commands
from discord_token import TOKEN
from VKbot import waiting
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from VK import VKToken, TGToken
from main import TG_bot
import random

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
        await ctx.send(ctx.message.author.mention + ' у тебя ' + str(self.users_list[str(ctx.message.author)]) + ' очков!')

    @commands.command(name='repeate')
    async def repeate_fraze(self, ctx, *text):
        if str(self.last_author) == str(ctx.message.author):
            for channel in ctx.guild.text_channels:
                if channel.name == 'bot_talking':
                    await channel.send('(' + str(ctx.author) + '): ' + ' '.join(text))

    @commands.command(name='give_id')
    async def give_id(self, ctx):
        for member in self.users_list.keys():
            if str(member) == ' '.join(ctx.message.content.split()[1:]):
                target = member
        try:
            await ctx.send(str(target.id))
        except Exception:
            await ctx.send('Пользователь не найден(')


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.users_list = {}
        self.last_author = ''
        super().__init__(*args, **kwargs)

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
        await self.send_in_chat(mes.content, str(mes.author))
        vk = vk_session.get_api()
        #vk.messages.send(chat_id=2,
        #                 message=f"""{update.message.from_user.username}:                    ##    Здесь нужно имя
        #                     {update.message.text}""",                                       ##    Здесь нужен текст
        #                 random_id=random.randint(0, 2 ** 64))

    async def on_member_join(self, member):
        print(member)

    async def send_in_chat(self, text, author):
        await self.crosschat.send('(' + author + '): ' + text)


bot = DiscordBot(command_prefix='!')
bot.add_cog(BotsCog(bot))

bot.run(TOKEN)