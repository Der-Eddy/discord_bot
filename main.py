import discord
from discord.ext import commands
import config
import logging
import asyncio
import random
import time

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discordbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Kleiner Test Bot in Python, einfach weil ichs kann'''
bot = commands.Bot(command_prefix=config.__prefix__, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_status(discord.Game(name=config.__game__))
    bot.load_extension('fun')
    bot.load_extension('admin')

@bot.command()
async def uptime():
    '''Wie lange bin ich schon online?'''
    timeUp = time.time() - startTime
    hoursUp = timeUp // 36000
    timeUp %= 36000
    minutesUp = (timeUp // 60) - (hoursUp * 60)
    timeUp = round(timeUp % 60, 0)
    msg = ":up: Ich bin online seit: *{0:n} Stunden, {1:n} Minuten und {2:n} Sekunden*".format(hoursUp, minutesUp, timeUp)
    await bot.say(msg)

@bot.command(pass_context=True)
async def test(ctx):
    '''Nur ein Test baka'''
    if ctx.message.author.id == config.__adminid__:
        await bot.say('Ja Meister?')
    else:
        await bot.say('Ich putze hier nur')

@bot.command(pass_context=True)
async def ping(ctx):
    '''Misst die Response Time'''
    ping = ctx.message
    pong = await bot.say(':ping_pong: Pong!')
    delta = pong.timestamp - ping.timestamp
    delta = int(delta.total_seconds() * 1000)
    await bot.edit_message(pong, ':ping_pong: Pong! ({0} ms)'.format(delta))

@bot.command()
async def github():
    '''Weil Open Source cool ist'''
    await bot.say('https://github.com/Der-Eddy/discord_bot')

@bot.command()
async def echo(*message):
    '''Gibt ne Nachricht aus'''
    msg = ':mega: ' + ' '.join(message)
    await bot.say(msg)

startTime = time.time()
bot.run(config.__token__)
