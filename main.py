import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
import asyncio
import random
import time
import platform
import datetime
from pytz import timezone

try:
    from config import __token__, __prefix__, __game__, __adminid__, __adminrole__, __modrole__, __kawaiichannel__, __botlogchannel__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __game__ = os.environ.get('DISCORD_GAME')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __adminrole__ = os.environ.get('DISCORD_ADMINROLE')
    __modrole__ = os.environ.get('DISCORD_MODROLE')
    __kawaiichannel__ = os.environ.get('DISCORD_KAWAIICHANNEL')
    __botlogchannel__ = os.environ.get('DISCORD_BOTLOGCHANNEL')
__version__ = '0.4.3'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename='discordbot.log', maxBytes=1024, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Eddys Chat Bot in Python, Discord.py rockt'''
bot = commands.Bot(command_prefix=__prefix__, description=description)

def _currenttime():
    return datetime.datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")

def _getRoles(roles):
    string = ''
    for r in roles:
        if not r.is_everyone:
            string += '{}, '.format(r.name)
    if string is '':
        return 'None'
    else:
        return string[:-2]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_status(discord.Game(name=__game__))
    bot.load_extension('fun')
    bot.load_extension('admin')
    bot.load_extension('anime')

@bot.event
async def on_member_join(member):
    memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
    await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:white_check_mark:** {1} tritt dem Server {2} bei'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_member_remove(member):
    memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
    await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:x:** {1} verließ den Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_server_join(server):
    serverExtra = '{0} - *Besitzer: {1} - Benutzer: {2} ({3})*'.format(server.name, server.owner, server.member_count, server.id)
    await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:white_check_mark:** Server {1} hinzugefügt'.format(_currenttime(), serverExtra))

@bot.event
async def on_server_remove(server):
    serverExtra = '{0} - *Besitzer: {1} - Benutzer: {2} ({3})*'.format(server.name, server.owner, server.member_count, server.id)
    await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:x:** Server {1} entfernt'.format(_currenttime(), serverExtra))

@bot.event
async def on_message_delete(message):
    member = message.author
    if not member.bot and not message.content.startswith(__prefix__) and not message.channel is bot.get_channel(__botlogchannel__): #Ignore messages from bots, commands and log channel
        memberExtra = '**{0} |** {1} *({2} - {3})*'.format(message.channel.mention, member, member.id, member.server)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:warning:** {1} löschte die Nachricht:\n ```{2}```'.format(_currenttime(), memberExtra, message.content))

@bot.event
async def on_message_edit(before, after):
    member = before.author
    if not member.bot and not before.content.startswith(__prefix__) and not after.edited_timestamp is None and not before.channel is bot.get_channel(__botlogchannel__): #Ignore messages from bots, commands and log channel
        memberExtra = '**{0} |** {1} *({2} - {3})*'.format(before.channel.mention, member, member.id, member.server)
        beforeContent = '**Before** - {0} ({1}):```{2}```'.format(before.author, before.timestamp, before.content)
        afterContent = '**After** - {0} ({1}):```{2}```'.format(after.author, after.edited_timestamp, after.content)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:information_source:** {1} änderte die Nachricht:\n {2} \n {3}'.format(_currenttime(), memberExtra, beforeContent, afterContent))

@bot.event
async def on_member_update(before, after):
    memberExtra = '**{0} |** {1} *({2} - {3})*'.format(before.mention, before, before.id, before.server)
    if len(before.roles) is not len(after.roles):
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:warning:** {1} Rollen wurden geändert:\n **Before:** `{2}`\n **After:** `{3}`'.format(_currenttime(), memberExtra, _getRoles(before.roles), _getRoles(after.roles)))
    elif before.nick is not after.nick:
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:information_source:** {1} Nickname wurde geändert:\n **Before:** `{2}`\n **After:** `{3}`'.format(_currenttime(), memberExtra, before.nick, after.nick))
    elif before.avatar is not after.avatar:
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:information_source:** {1} Avatar wurde geändert:\n **Before:** {2}\n **After:** {3}'.format(_currenttime(), memberExtra, before.avatar_url, after.avatar_url))

@bot.event
async def on_member_ban(member):
    memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
    await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:customs:** {1} wurde gebannt auf Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_member_unban(member):
    memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
    await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:negative_squared_cross_mark:** {1} wurde entbannt auf Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.command()
async def status():
    '''Infos über den Bot'''
    hours, minutes, seconds = _uptime()

    admin = ''
    users = 0
    for s in bot.servers:
        users += len(s.members)
        if not admin: admin = s.get_member(__adminid__)

    msg = '**:information_source:** Informationen über diesen Bot:\n'
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
    msg = '**:up:** Ich bin online seit: *{0:.0f} Stunden, {1:.0f} Minuten und {2:.0f} Sekunden*'.format(hours, minutes, seconds)
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
    pong = await bot.say('**:ping_pong:** Pong!')
    delta = pong.timestamp - ping.timestamp
    delta = int(delta.total_seconds() * 1000)
    await bot.edit_message(pong, '**:ping_pong:** Pong! (%d ms)' % delta)

@bot.command()
async def github():
    '''Weil Open Source cool ist'''
    await bot.say('**:free:** https://github.com/Der-Eddy/discord_bot')

@bot.command(pass_context=True)
async def echo(ctx, *message):
    '''Gibt ne Nachricht aus'''
    msg = '**:mega:** ' + ' '.join(message)
    await bot.say(msg)
    await bot.delete_message(ctx.message)

startTime = time.time()
bot.run(__token__)
