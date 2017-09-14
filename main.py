import logging
from logging.handlers import RotatingFileHandler
import random
import sqlite3
import traceback
import time
import datetime
import sys
import os
import hashlib
import asyncio
import aiohttp
from collections import Counter
from pytz import timezone
import discord
from discord.ext import commands
import loadconfig

__version__ = '0.17.5'

logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)
handler = RotatingFileHandler(filename='discordbot.log', maxBytes=1024*5, backupCount=2, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Der-Eddys deutscher Discord Bot, programmiert mit Discord.py\n
                 Eine volle Liste aller Commands gibts hier: https://github.com/Der-Eddy/discord_bot#commands-list'''
bot = commands.Bot(command_prefix=loadconfig.__prefix__, description=description)

def _currenttime():
    return datetime.datetime.now(timezone('Europe/Berlin')).strftime('%H:%M:%S')

async def _randomGame():
    #Check games.py to change the list of "games" to be played
    while True:
        serverCount = len(bot.servers)
        memberCount = len(list(bot.get_all_members()))
        randomGame = random.choice(loadconfig.__games__).format(servers = serverCount, members = memberCount)
        logging.info(f'Changing name to {randomGame}')
        await bot.change_presence(game=discord.Game(name=randomGame))
        await asyncio.sleep(loadconfig.__gamesTimer__)

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

def _getHash(downloadedFile, hashAlgorithm=hashlib.sha256()):
        blocksize = 65536
        algo = hashAlgorithm
        with open(downloadedFile, 'rb') as file:
            buffer = file.read(blocksize)
            while len(buffer) > 0:
                algo.update(buffer)
                buffer = file.read(blocksize)
        return algo.hexdigest()

async def _fileCheck(msg):
    url = msg.attachments[0]['url']
    allowedExtension = ['.exe', '.zip', '.rar']
    if url[-4:] in allowedExtension:
        name = os.path.basename(url)
        downloadPath = 'tmp\\' + name
        async with aiohttp.get(url) as download:
            with open(downloadPath, 'wb') as f:
                f.write(await download.read())
        stats = os.stat(downloadPath)
        size = stats.st_size
        KBSize = round(size / 1024, 3)
        MBSize = round(size / 1024 / 1024, 3)
        MD5 = _getHash(downloadPath, hashlib.md5())
        SHA1 = _getHash(downloadPath, hashlib.sha1())
        SHA256 = _getHash(downloadPath, hashlib.sha256())
        SHA512 = _getHash(downloadPath, hashlib.sha512())
        msg = f'**Name:** {name}\n'
        msg += f'**Size:** {MBSize} MB ({size} Bytes)\n'
        msg += f'**MD5:** `{MD5}`\n'
        msg += f'**SHA1:** `{SHA1}`\n'
        msg += f'**SHA256:** `{SHA256}`\n'
        msg += f'**SHA512:** `{SHA512}`\n'
        os.remove(downloadPath)
        return msg

@bot.event
async def on_ready():
    print('Logged in as')
    print(f'Bot-Name: {bot.user.name}')
    print(f'Bot-ID: {bot.user.id}')
    if bot.user.id == '204966267147255808':
        bot.dev = True
    else:
        bot.dev = False
    print(f'Dev Mode: {bot.dev}')
    print('------')
    for cog in loadconfig.__cogs__:
        try:
            bot.load_extension(cog)
        except Exception:
            print(f'Couldn\'t load cog {cog}')
    bot.commands_used = Counter()
    bot.startTime = time.time()
    bot.botVersion = __version__
    bot.userAgentHeaders = {'User-Agent': f'linux:shinobu_discordbot:v{__version__} (by Der-Eddy)'}
    bot.owner = discord.utils.find(lambda u: u.id == loadconfig.__adminid__, bot.get_all_members())
    bot.gamesLoop = asyncio.ensure_future(_randomGame())
    _setupDatabase('reaction.db')

@bot.event
async def on_command(command, ctx):
    bot.commands_used[command.name] += 1
    msg = ctx.message
    if msg.channel.is_private:
        destination = 'Private Message'
    else:
        destination = f'#{msg.channel.name} ({msg.server.name})'
    logging.info(f'{msg.timestamp}: {msg.author.name} in {destination}: {msg.content}')

@bot.event
async def on_message(message):
    if message.author.bot or message.author.id in loadconfig.__blacklist__ or message.server.id == '110373943822540800':
        return
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        if 'help' in message.content.lower():
            await bot.send_message(message.channel, 'Eine volle Liste aller Commands gibts hier: https://github.com/Der-Eddy/discord_bot#commands-list')
        else:
            await bot.add_reaction(message, '👀') # :eyes:
    if 'loli' in message.clean_content.lower():
        await bot.add_reaction(message, '🍭') # :lollipop:
    if 'instagram.com' in message.clean_content.lower():
        await bot.add_reaction(message, '💩') # :poop:
    if len(message.attachments) > 0:
        try:
            await bot.send_message(message.channel, await _fileCheck(message))
        except:
            pass
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    if member.server.id == loadconfig.__botserverid__ and not bot.dev:
        if member.id in loadconfig.__blacklist__:
            bot.kick(member)
            await bot.send_message(bot.owner, f'Benutzer **{member}** automatisch gekickt')
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        if loadconfig.__greetmsg__ == 'True':
            emojis = [':wave:', ':congratulations:', ':wink:', ':new:', ':cool:', ':white_check_mark:', ':tada:']
            await bot.send_message(member.server.default_channel, '{0} Willkommen {1} auf Der-Eddys Discord Server! Für weitere Informationen, wie unsere nsfw Channel :underage: , besuche unseren <#165973433086115840> Channel.'.format(random.choice(emojis), member.mention))

@bot.event
async def on_member_remove(member):
    if member.server.id == loadconfig.__botserverid__ and not bot.dev:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        if loadconfig.__greetmsg__ == 'True':
            await bot.send_message(member.server.default_channel, f'<:faeSad:298772756127023104> **{member.name}** verließ unseren Server.')

@bot.event
async def on_server_join(server):
    embed = discord.Embed(title=':white_check_mark: Server hinzugefügt', type='rich', color=0x2ecc71) #Green
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name='Name', value=server.name, inline=True)
    embed.add_field(name='ID', value=server.id, inline=True)
    embed.add_field(name='Besitzer', value=f'{server.owner} ({server.owner.id})', inline=True)
    embed.add_field(name='Region', value=server.region, inline=True)
    embed.add_field(name='Mitglieder', value=server.member_count, inline=True)
    embed.add_field(name='Erstellt am', value=server.created_at, inline=True)
    await bot.send_message(bot.owner, embed=embed)

@bot.event
async def on_server_remove(server):
    embed = discord.Embed(title=':x: Server entfernt', type='rich', color=0xe74c3c) #Red
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name='Name', value=server.name, inline=True)
    embed.add_field(name='ID', value=server.id, inline=True)
    embed.add_field(name='Besitzer', value=f'{server.owner} ({server.owner.id})', inline=True)
    embed.add_field(name='Region', value=server.region, inline=True)
    embed.add_field(name='Mitglieder', value=server.member_count, inline=True)
    embed.add_field(name='Erstellt am', value=server.created_at, inline=True)
    await bot.send_message(bot.owner, embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    if bot.dev:
        traceback.print_exc()
    else:
        embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        try:
            await bot.send_message(bot.owner, embed=embed)
        except:
            pass

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.say(':x: Dieser Command wurde deaktiviert')
    elif isinstance(error, commands.CommandInvokeError):
        if bot.dev:
            raise error
        else:
            embed = discord.Embed(title=':x: Command Error', colour=0x992d22) #Dark Red
            embed.add_field(name='Error', value=error)
            embed.add_field(name='Server', value=ctx.message.server)
            embed.add_field(name='Channel', value=ctx.message.channel)
            embed.add_field(name='User', value=ctx.message.author)
            embed.add_field(name='Message', value=ctx.message.clean_content)
            embed.timestamp = datetime.datetime.utcnow()
            try:
                await bot.send_message(bot.owner, embed=embed)
            except:
                pass

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
