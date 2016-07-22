import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
import asyncio
import random
import time
import platform

try:
    from config import __token__, __prefix__, __game__, __adminid__, __adminrole__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __game__ = os.environ.get('DISCORD_GAME')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __adminrole__ = os.environ.get('DISCORD_ADMINROLE')
__version__ = '0.2.3'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename='discordbot.log', maxBytes=1024, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Kleiner Chat Bot in Python, Discord.py rockt'''
bot = commands.Bot(command_prefix=__prefix__, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_status(discord.Game(name=__game__))
    bot.load_extension('fun')
    bot.load_extension('admin')

@bot.command()
async def status():
    '''Infos über den Bot'''
    hours, minutes, seconds = _uptime()

    admin = ''
    users = 0
    for s in bot.servers:
        users += len(s.members)
        if not admin: admin = s.get_member(__adminid__)

    msg = ':information_source: Informationen über diesen Bot:\n'
    msg += '```Admin              : @%s\n' % admin
    msg += 'Uptime             : {0:.0f} Stunden, {1:.0f} Minuten und {2:.0f} Sekunden\n'.format(hours, minutes, seconds)
    msg += 'Benutzer / Server  : %s in %s Server\n' % (users, len(bot.servers))
    msg += 'Bot Version        : %s\n' % __version__
    msg += 'Discord.py Version : %s\n' % discord.__version__
    msg += 'Python Version     : %s\n' % platform.python_version()
    msg += 'GitHub             : https://github.com/Der-Eddy/discord_bot```'
    await bot.say(msg)

@bot.command()
async def uptime():
    '''Wie lange bin ich schon online?'''
    hours, minutes, seconds = _uptime()
    msg = ':up: Ich bin online seit: *{0:.0f} Stunden, {1:.0f} Minuten und {2:.0f} Sekunden*'.format(hours, minutes, seconds)
    await bot.say(msg)

def _uptime():
    timeUp = time.time() - startTime
    hours = timeUp / 3600
    minutes = (timeUp / 60) % 60
    seconds = timeUp % 60
    return hours, minutes, seconds

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
    await bot.edit_message(pong, ':ping_pong: Pong! (%d ms)' % delta)

@bot.command()
async def github():
    '''Weil Open Source cool ist'''
    await bot.say(':free: https://github.com/Der-Eddy/discord_bot')

@bot.command(pass_context=True)
async def echo(ctx, *message):
    '''Gibt ne Nachricht aus'''
    msg = ':mega: ' + ' '.join(message)
    await bot.say(msg)
    await bot.delete_message(ctx.message)

startTime = time.time()
bot.run(__token__)
