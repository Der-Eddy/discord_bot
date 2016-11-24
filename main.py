import logging
from logging.handlers import RotatingFileHandler
import random
import time
import datetime
import sys
import asyncio
from collections import Counter
from pytz import timezone
import discord
from discord.ext import commands
import loadconfig

__version__ = '0.10.1'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename='discordbot.log', maxBytes=1024, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Der-Eddys deutscher Discord Bot, programmiert mit Discord.py'''
bot = commands.Bot(command_prefix=loadconfig.__prefix__, description=description)

def _currenttime():
    return datetime.datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")

async def _randomGame():
    #Check games.py to change the list of "games" to be played
    while True:
        await bot.change_presence(game=discord.Game(name=random.choice(loadconfig.__games__)))
        await asyncio.sleep(loadconfig.__gamesTimer__)

@bot.event
async def on_ready():
    print('Logged in as')
    print('Bot-Name: {}'.format(bot.user.name))
    print('Bot-ID: {}'.format(bot.user.id))
    print('------')
    for cog in loadconfig.__cogs__:
        try:
            bot.load_extension(cog)
        except Exception:
            print('Couldn\'t load cog {}'.format(cog))
    bot.commands_used = Counter()
    bot.startTime = time.time()
    bot.botVersion = __version__
    asyncio.ensure_future(_randomGame())

@bot.event
async def on_command(command, ctx):
    bot.commands_used[command.name] += 1
    msg = ctx.message
    if msg.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(msg)
    logging.info('{0.timestamp}: {0.author.name} in {1}: {0.content}'.format(msg, destination))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    if member.server.id == loadconfig.__botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:white_check_mark:** {1} tritt dem Server {2} bei'.format(_currenttime(), memberExtra, member.server))
        if __greetmsg__ == 'True':
            emojis = [':wave:', ':congratulations:', ':wink:', ':new:', ':cool:', ':white_check_mark:', ':tada:']
            await bot.send_message(member.server.default_channel, '{0} Willkommen {1} auf Der-Eddys Discord Server! Für weitere Informationen, wie unsere nsfw Channel :underage: , besuche unseren <#165973433086115840> Channel.'.format(random.choice(emojis), member.mention))

@bot.event
async def on_member_remove(member):
    if member.server.id == loadconfig.__botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:x:** {1} verließ den Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_server_join(server):
    serverExtra = '{0} - *Besitzer: {1} - Benutzer: {2} ({3})*'.format(server.name, server.owner, server.member_count, server.id)
    await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:white_check_mark:** Server {1} hinzugefügt'.format(_currenttime(), serverExtra))

@bot.event
async def on_server_remove(server):
    serverExtra = '{0} - *Besitzer: {1} - Benutzer: {2} ({3})*'.format(server.name, server.owner, server.member_count, server.id)
    await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:x:** Server {1} entfernt'.format(_currenttime(), serverExtra))

@bot.event
async def on_message_delete(message):
    member = message.author
    if member.server.id == loadconfig.__botserverid__:
        if not member.bot and not message.content.startswith(loadconfig.__prefix__) and not message.channel is bot.get_channel(loadconfig.__botlogchannel__): #Ignore messages from bots, commands and log channel, my test bot also uses the ; prefix
            memberExtra = '**{0} |** {1} *({2} - {3})*'.format(message.channel.mention, member, member.id, member.server)
            await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:warning:** {1} löschte die Nachricht:\n ```{2}```'.format(_currenttime(), memberExtra, message.content))

@bot.event
async def on_message_edit(before, after):
    member = before.author
    if member.server.id == loadconfig.__botserverid__:
        if not member.bot and not before.content.startswith(loadconfig.__prefix__) and not before.content.startswith(';') and not after.edited_timestamp is None and not before.channel is bot.get_channel(loadconfig.__botlogchannel__): #Ignore messages from bots, commands and log channel
            memberExtra = '**{0} |** {1} *({2} - {3})*'.format(before.channel.mention, member, member.id, member.server)
            beforeContent = '**Before** - {0} ({1}):```{2}```'.format(before.author, before.timestamp, before.content)
            afterContent = '**After** - {0} ({1}):```{2}```'.format(after.author, after.edited_timestamp, after.content)
            await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:information_source:** {1} änderte die Nachricht:\n {2} \n {3}'.format(_currenttime(), memberExtra, beforeContent, afterContent))

@bot.event
async def on_member_update(before, after):
    if before.server.id == loadconfig.__botserverid__:
        memberExtra = '**{0} |** {1} *({2} - {3})*'.format(before.mention, before, before.id, before.server)
        if len(before.roles) is not len(after.roles):
            await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:warning:** {1} Rollen wurden geändert:\n **Before:** `{2}`\n **After:** `{3}`'.format(_currenttime(), memberExtra, _getRoles(before.roles), _getRoles(after.roles)))
        elif before.nick is not after.nick:
            await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:information_source:** {1} Nickname wurde geändert:\n **Before:** `{2}`\n **After:** `{3}`'.format(_currenttime(), memberExtra, before.nick, after.nick))
        elif before.avatar_url is not after.avatar_url and False:
            await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:information_source:** {1} Avatar wurde geändert:\n **Before:** {2}\n **After:** {3}'.format(_currenttime(), memberExtra, before.avatar_url, after.avatar_url))

@bot.event
async def on_member_ban(member):
    if member.server.id == loadconfig.__botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:customs:** {1} wurde gebannt auf Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.event
async def on_member_unban(member):
    if member.server.id == loadconfig.__botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        await bot.send_message(bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:negative_squared_cross_mark:** {1} wurde entbannt auf Server {2}'.format(_currenttime(), memberExtra, member.server))

@bot.command(pass_context=True, hidden=True, aliases=['quit_backup'])
async def shutdown_backup(ctx):
    '''Fallback if mod cog couldn't load'''
    if ctx.message.author.id == loadconfig.__adminid__:
        await bot.say('**:ok:** Bye!')
        bot.logout()
        sys.exit(0)
    else:
        await bot.say('**:no_entry:** Du bist nicht mein Bot Besitzer!')

if __name__ == '__main__':
    bot.run(loadconfig.__token__)
