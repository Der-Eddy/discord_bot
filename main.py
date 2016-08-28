import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
import asyncio
import aiohttp
import random
import time
import platform
import datetime
import sqlite3
import xml.etree.ElementTree as ET
from pytz import timezone
from io import UnsupportedOperation
from games import __games__, __gamesTimer__

try:
    from config import __token__, __prefix__, __adminid__, __adminrole__, __modrole__, __kawaiichannel__, __botlogchannel__, __github__, __botserverid__, __greetmsg__, __selfassignrole__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __botserverid__ = os.environ.get('DISCORD_BOTSERVERID')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __adminrole__ = os.environ.get('DISCORD_ADMINROLE')
    __modrole__ = os.environ.get('DISCORD_MODROLE')
    __kawaiichannel__ = os.environ.get('DISCORD_KAWAIICHANNEL')
    __botlogchannel__ = os.environ.get('DISCORD_BOTLOGCHANNEL')
    __github__ = os.environ.get('DISCORD_GITHUB')
    __greetmsg__ = os.environ.get('DISCORD_GREETMSG')
    __selfassignrole__ = os.environ.get('DISCORD_SELFASSIGNROLE')
__version__ = '0.6.10'

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

def _setupDatabase(db):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS `reactions` (
                    	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    	`command`	TEXT NOT NULL,
                    	`url`	TEXT NOT NULL UNIQUE,
                    	`author`	TEXT
                    );''')
        con.commit()
        c.close()

async def _randomGame():
    #Check games.py to change the list of "games" to be played
    while True:
        await bot.change_status(discord.Game(name=random.choice(__games__)))
        await asyncio.sleep(__gamesTimer__)

async def _githubLog():
    #Logs new commits to a hardcoded channel
    if __github__ == 'True':
        devChannel = bot.get_channel('165156137476292608')
        authorAndRepo = 'Der-Eddy/discord_bot'
        url = 'https://api.github.com/repos/%s/commits' % authorAndRepo
        while True:
            with open('tempBot.txt', 'a+') as temp:
                temp.seek(0)
                oldHash = temp.read()
            async with aiohttp.get(url) as resp:
                r = await resp.json()
            if not oldHash == r[0]['sha'] and r[0]['sha'] != '':
                with open('tempBot.txt', 'w+') as temp:
                    temp.write(r[0]['sha'])
                msg = ':cool: Ein neuer Commit für **{0}**!\n **Author:** `{1}`\n **Date:** `{2}`\n **Commit:** `#{3}` - {4}\n **Commit Message:** ```{5}```'.format(authorAndRepo, r[0]['commit']['author']['name'], r[0]['commit']['author']['date'], r[0]['sha'][:7], r[0]['html_url'], r[0]['commit']['message'])
                await bot.send_message(devChannel, msg)
            await asyncio.sleep(60)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.load_extension('fun')
    bot.load_extension('mod')
    bot.load_extension('anime')
    asyncio.ensure_future(_randomGame())
    asyncio.ensure_future(_githubLog())
    _setupDatabase('reaction.db')

@bot.event
async def on_member_join(member):
    if member.server.id == __botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:white_check_mark:** {1} tritt dem Server {2} bei'.format(_currenttime(), memberExtra, member.server))
        if __greetmsg__ == 'True':
            emojis = [':wave:', ':congratulations:', ':wink:', ':new:', ':cool:', ':white_check_mark:', ':tada:']
            await bot.send_message(member.server.default_channel, '{0} Willkommen {1} auf Der-Eddys Discord Server! Für weitere Informationen, wie unsere nsfw Channel :underage: , besuche unseren <#165973433086115840> Channel.'.format(random.choice(emojis), member.mention))

@bot.event
async def on_member_remove(member):
    if member.server.id == __botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:x:** {1} verließ den Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_server_join(server):
    if server.id == __botserverid__:
        serverExtra = '{0} - *Besitzer: {1} - Benutzer: {2} ({3})*'.format(server.name, server.owner, server.member_count, server.id)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:white_check_mark:** Server {1} hinzugefügt'.format(_currenttime(), serverExtra))

@bot.event
async def on_server_remove(server):
    if server.id == __botserverid__:
        serverExtra = '{0} - *Besitzer: {1} - Benutzer: {2} ({3})*'.format(server.name, server.owner, server.member_count, server.id)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:x:** Server {1} entfernt'.format(_currenttime(), serverExtra))

@bot.event
async def on_message_delete(message):
    member = message.author
    if member.server.id == __botserverid__:
        if not member.bot and not message.content.startswith(__prefix__) and not message.channel is bot.get_channel(__botlogchannel__): #Ignore messages from bots, commands and log channel, my test bot also uses the ; prefix
            memberExtra = '**{0} |** {1} *({2} - {3})*'.format(message.channel.mention, member, member.id, member.server)
            await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:warning:** {1} löschte die Nachricht:\n ```{2}```'.format(_currenttime(), memberExtra, message.content))

@bot.event
async def on_message_edit(before, after):
    member = before.author
    if member.server.id == __botserverid__:
        if not member.bot and not before.content.startswith(__prefix__) and not before.content.startswith(';') and not after.edited_timestamp is None and not before.channel is bot.get_channel(__botlogchannel__): #Ignore messages from bots, commands and log channel
            memberExtra = '**{0} |** {1} *({2} - {3})*'.format(before.channel.mention, member, member.id, member.server)
            beforeContent = '**Before** - {0} ({1}):```{2}```'.format(before.author, before.timestamp, before.content)
            afterContent = '**After** - {0} ({1}):```{2}```'.format(after.author, after.edited_timestamp, after.content)
            await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:information_source:** {1} änderte die Nachricht:\n {2} \n {3}'.format(_currenttime(), memberExtra, beforeContent, afterContent))

@bot.event
async def on_member_update(before, after):
    if before.server.id == __botserverid__:
        memberExtra = '**{0} |** {1} *({2} - {3})*'.format(before.mention, before, before.id, before.server)
        if len(before.roles) is not len(after.roles):
            await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:warning:** {1} Rollen wurden geändert:\n **Before:** `{2}`\n **After:** `{3}`'.format(_currenttime(), memberExtra, _getRoles(before.roles), _getRoles(after.roles)))
        elif before.nick is not after.nick:
            await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:information_source:** {1} Nickname wurde geändert:\n **Before:** `{2}`\n **After:** `{3}`'.format(_currenttime(), memberExtra, before.nick, after.nick))
        elif before.avatar_url is not after.avatar_url and False:
            await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:information_source:** {1} Avatar wurde geändert:\n **Before:** {2}\n **After:** {3}'.format(_currenttime(), memberExtra, before.avatar_url, after.avatar_url))

@bot.event
async def on_member_ban(member):
    if member.server.id == __botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:customs:** {1} wurde gebannt auf Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_member_unban(member):
    if member.server.id == __botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(__botlogchannel__), '`[{0}]` **:negative_squared_cross_mark:** {1} wurde entbannt auf Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.command(aliases=['s', 'uptime', 'up'])
async def status():
    '''Infos über den Bot'''
    timeUp = time.time() - startTime
    hours = timeUp / 3600
    minutes = (timeUp / 60) % 60
    seconds = timeUp % 60

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

@bot.command(pass_context=True, aliases=['p'])
async def ping(ctx):
    '''Misst die Response Time'''
    ping = ctx.message
    pong = await bot.say('**:ping_pong:** Pong!')
    delta = pong.timestamp - ping.timestamp
    delta = int(delta.total_seconds() * 1000)
    await bot.edit_message(pong, '**:ping_pong:** Pong! (%d ms)' % delta)

@bot.command(pass_context=True, aliases=['info', 'github', 'trello'])
async def about(ctx):
    '''Info über mich'''
    msg = '**:information_source: Shinobu Oshino (500 Jahre alt)**\n'
    msg += '```Shinobu Oshino gehört wohl zu den mysteriösesten Charakteren in Bakemonogatari. Sie war bis vorletzten Frühling ein hochangesehener, adeliger, skrupelloser Vampir, der weit über 500 Jahre alt ist. Gnadenlos griff sie Menschen an und massakrierte sie nach Belieben. Auch Koyomi Araragi wurde von ihr attackiert und schwer verwundet. Nur durch das Eingreifen des Exorzisten Meme Oshino konnte Kiss-shot Acerola-orion Heart-under-blade, wie sie damals bekannt war, bezwungen werden. Dabei verlor sie jedoch all ihre Erinnerungen und wurde von einer attraktiven, erwachsenen Frau in einen unschuldigen Mädchenkörper verwandelt.\n\n'
    msg += 'Seitdem lebt sie zusammen mit Meme in einem verlassenen Gebäude und wurde von ihm aufgenommen. Er gab ihr auch ihren Namen Shinobu. Wann immer man Shinobu sehen sollte, sitzt sie nur mit traurigem Gesicht in einer Ecke und träumt vor sich hin. Sie spricht nicht und wirkt auch sonst meistens sehr abwesend. Einzig und allein zu Koyomi scheint sie ein freundschaftliches Verhältnis zu haben. Das Vampirblut in ihr verlangt immer noch nach Opfern und da sich Koyomi in gewisser Art und Weise schuldig fühlt, stellt er sich regelmäßig als Nahrungsquelle für Shinobu zur Verfügung.\n\n'
    msg += 'Quelle: http://www.anisearch.de/character/6598,shinobu-oshino/```\n\n'
    msg += 'Dieser Bot ist außerdem **:free:**, Open-Source, in Python und mit Hilfe von discord.py geschrieben! <https://github.com/Der-Eddy/discord_bot>\n'
    msg += 'Neueste Neuerungen immer zuerst auf unserem Trello Board! <https://trello.com/b/Kh8nfuBE/discord-bot-shinobu-chan>'
    with open('img/ava.png', 'rb') as f:
        await bot.send_file(ctx.message.channel, f, content=msg)

@bot.command(pass_context=True)
async def echo(ctx, *message):
    '''Gibt ne Nachricht aus'''
    msg = '**:mega:** ' + ' '.join(message)
    await bot.say(msg)
    await bot.delete_message(ctx.message)

@bot.command()
async def whois(member: discord.Member = None):
    '''Gibt Informationen über einen Benutzer aus

    Beispiel:
    -----------

    :whois @Der-Eddy#6508
    '''

    if member.top_role.is_everyone:
        topRole = 'everyone aka None' #to prevent @everyone spam
        topRoleColour = '#000000'
    else:
        topRole = member.top_role
        topRoleColour = member.top_role.colour

    if member is not None:
        msg = '**:information_source:** Informationen über %s:\n' % member
        msg += '```General              : %s\n' % member
        msg += 'Name                 : %s\n' % member.name
        msg += 'Server Nickname      : %s\n' % member.display_name
        msg += 'Discriminator        : %s\n' % member.discriminator
        msg += 'ID                   : %s\n' % member.id
        msg += 'Bot Account?         : %s\n' % member.bot
        msg += 'Avatar               : %s\n' % member.avatar_url
        msg += 'Erstellt am          : %s\n' % member.created_at
        msg += 'Server beigetreten am: %s\n' % member.joined_at
        msg += 'Rollenfarbe          : %s (%s)\n' % (topRoleColour, topRole)
        msg += 'Status               : %s\n' % member.status
        msg += 'Rollen               : %s```' % _getRoles(member.roles)
    else:
        msg = '**:no_entry:** Du hast keinen Benutzer angegeben!'
    await bot.say(msg)

@bot.command(aliases=['epvp'])
async def epvpis(*user: str):
    '''Sucht nach einem Benutzernamen auf Elitepvpers

    Beispiel:
    -----------

    :epvpis Der-Eddy
    '''
    user = ' '.join(user)
    url = 'https://www.elitepvpers.com/forum/ajax.php?do=usersearch'
    payload = {
        'do': 'usersearch',
        'fragment': user
    }
    async with aiohttp.post(url, data=payload) as r:
        if r.status == 200:
            root = ET.fromstring(await r.text())
            if len(root) > 0:
                msg = ':ok: Ich konnte {} Accounts finden!\n```'.format(len(root))
                for i in root:
                    userURL = 'https://www.elitepvpers.com/forum/member.php?u=' + i.attrib['userid']
                    msg += '{} | {}\n'.format(i.text, userURL)
                msg += '```'
            else:
                msg = ':no_entry: Ich konnte keine Epvp Accounts finden :sweat:'
            await bot.say(msg)

startTime = time.time()
bot.run(__token__)
