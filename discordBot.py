import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
TOKEN = 'OTUxNDgzNDEzNDk4NTc2OTg2.YioH-w.uJDuDQNA_uz8EvizbpsxpfHrH-Q'

users = {}

@bot.event
async def on_ready():
    for g in bot.guilds:
        for c in g.text_channels:
            await c.send('here i am')
        for m in g.members:
            if m.name not in users:
                users[str(m)] = 0
    print(users)

@bot.command(name='test')
async def test(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            print(member)
            users[str(member)] = 0
    print(users)
    await ctx.send('What???')

@bot.command()
async def очки(ctx):
    await ctx.send(ctx.message.author.mention + ' у тебя ' + str(users[str(ctx.message.author)]) + ' очков!')

"""@bot.event
async def on_message(mes):
    pass
    if mes.author == bot.user:
        return
    users[str(mes.author)] += 1

    if mes.content[0] != '!':
        pass
    else:
        await bot.process_commands(mes)"""

@bot.event
async def on_member_join(member):
    users[str(member.author)] = 0
    print(users)

bot.run(TOKEN)