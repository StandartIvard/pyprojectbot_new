import discord
from discord.ext import commands
from discord_token import TOKEN


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
        if bot.last_author == str(ctx.message.author):
            for channel in ctx.guild.text_channels:
                if channel.name == 'bot_talking':
                    await channel.send('(' + str(ctx.author) + '): ' + ' '.join(text))

    @commands.command(name='give_id')
    async def give_id(self, ctx):
        for member in bot.users_list.keys():
            if str(member) == ctx.message.content.split()[1:]:
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
        for g in bot.guilds:
            for c in g.text_channels:
                await c.send('here i am')
            for m in g.members:
                if m.name not in self.users_list:
                    self.users_list[m] = 0

    async def on_message(self, mes):
        if mes.author == bot.user:
            return
        if mes.author not in self.users_list:
            self.users_list[mes.author] = 0
        self.users_list[mes.author] += 1
        if mes.content.startswith('!'):
            await bot.process_commands(mes)
        self.last_author = mes.author

    async def on_member_join(self, member):
        print(member)


bot = DiscordBot(command_prefix='!')
bot.add_cog(BotsCog(bot))

bot.run(TOKEN)