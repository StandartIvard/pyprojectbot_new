import discord
from discord.ext import commands


class BotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('What???')

    @commands.command(name='points')
    async def points(self, ctx):
        await ctx.send(ctx.message.author.mention + ' у тебя ' + str(bot.users_list[str(ctx.message.author)]) + ' очков!')


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.users_list = {}
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        for g in bot.guilds:
            for c in g.text_channels:
                await c.send('here i am')
            for m in g.members:
                if m.name not in self.users_list:
                    self.users_list[str(m)] = 0

    async def on_message(self, mes):
        if mes.author == bot.user:
            return
        if str(mes.author) not in self.users_list:
            self.users_list[str(mes.author)] = 0
        self.users_list[str(mes.author)] += 1
        if mes.content.startswith('!'):
            await bot.process_commands(mes)

    async def on_member_join(self, member):
        print(member)


bot = DiscordBot(command_prefix='!')
bot.add_cog(BotsCog(bot))

TOKEN = 'OTUxNDgzNDEzNDk4NTc2OTg2.YioH-w.uJDuDQNA_uz8EvizbpsxpfHrH-Q'

bot.run(TOKEN)