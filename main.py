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

__version__ = '1.1.0'

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
        guildCount = len(bot.guilds)
        memberCount = len(list(bot.get_all_members()))
        randomGame = random.choice(loadconfig.__games__)
        await bot.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds = guildCount, members = memberCount)))
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

@bot.event
async def on_ready():
    if bot.user.id == 204966267147255808:
        bot.dev = True
    else:
        bot.dev = False

    print('Logged in as')
    print(f'Bot-Name: {bot.user.name}')
    print(f'Bot-ID: {bot.user.id}')
    print(f'Dev Mode: {bot.dev}')
    print(f'Discord Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')
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
    bot.gamesLoop = asyncio.ensure_future(_randomGame())
    _setupDatabase('reaction.db')

@bot.event
async def on_command(ctx):
    bot.commands_used[ctx.command.name] += 1
    msg = ctx.message
    # if isinstance(msg.channel, discord.Channel):
    #     #dest = f'#{msg.channel.name} ({msg.guild.name})'
    #     dest = f'#{msg.channel.name}'
    # elif isinstance(msg.channel, discord.DMChannel):
    #     dest = 'Direct Message'
    # elif isinstance(msg.channel, discord.GroupChannel):
    #     dest = 'Group Message'
    # else:
    #     dest = 'Voice Channel'
    # logging.info(f'{msg.created_at}: {msg.author.name} in {dest}: {msg.content}')

@bot.event
async def on_message(message):
    if message.author.bot or message.author.id in loadconfig.__blacklist__:
        return
    if isinstance(message.channel, discord.DMChannel):
        await message.author.send(':x: Sorry, but I don\'t accept commands through direct messages! Please use the `#bots` channel of your corresponding server!')
        return
    if bot.dev and not await bot.is_owner(message.author):
        return
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        if 'help' in message.content.lower():
            await message.channel.send('Eine volle Liste aller Commands gibts hier: https://github.com/Der-Eddy/discord_bot#commands-list')
        else:
            await message.add_reaction('👀') # :eyes:
    if 'loli' in message.clean_content.lower():
        await message.add_reaction('🍭') # :lollipop:
    if 'instagram.com' in message.clean_content.lower():
        await message.add_reaction('💩') # :poop:
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    if member.guild.id == loadconfig.__botserverid__ and not bot.dev:
        if member.id in loadconfig.__blacklist__:
            member.kick()
            await bot.owner.send(f'Benutzer **{member}** automatisch gekickt')
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        if loadconfig.__greetmsg__ != 0:
            channel = member.guild.get_channel(loadconfig.__greetmsg__)
            emojis = [':wave:', ':congratulations:', ':wink:', ':new:', ':cool:', ':white_check_mark:', ':tada:']
            await channel.send('{0} Willkommen {1} auf Der-Eddys Discord Server! Für weitere Informationen, wie unsere nsfw Channel :underage: , besuche unseren <#165973433086115840> Channel.'.format(random.choice(emojis), member.mention))
    elif member.guild.id == 161637499939192832:
        rank = discord.utils.get(member.guild.roles, name='Member')
        await member.add_roles(rank)

@bot.event
async def on_member_remove(member):
    if member.guild.id == loadconfig.__botserverid__ and not bot.dev:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        if loadconfig.__greetmsg__ != 0:
            channel = member.guild.get_channel(loadconfig.__greetmsg__)
            await channel.send(f'<:faeSad:298772756127023104> **{member.name}** verließ unseren Server.')

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(title=':white_check_mark: Guild hinzugefügt', type='rich', color=0x2ecc71) #Green
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name='Name', value=guild.name, inline=True)
    embed.add_field(name='ID', value=guild.id, inline=True)
    embed.add_field(name='Besitzer', value=f'{guild.owner} ({guild.owner.id})', inline=True)
    embed.add_field(name='Region', value=guild.region, inline=True)
    embed.add_field(name='Mitglieder', value=guild.member_count, inline=True)
    embed.add_field(name='Erstellt am', value=guild.created_at, inline=True)
    await bot.owner.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(title=':x: Guild entfernt', type='rich', color=0xe74c3c) #Red
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name='Name', value=guild.name, inline=True)
    embed.add_field(name='ID', value=guild.id, inline=True)
    embed.add_field(name='Besitzer', value=f'{guild.owner} ({guild.owner.id})', inline=True)
    embed.add_field(name='Region', value=guild.region, inline=True)
    embed.add_field(name='Mitglieder', value=guild.member_count, inline=True)
    embed.add_field(name='Erstellt am', value=guild.created_at, inline=True)
    await bot.owner.send(embed=embed)

# @bot.event
# async def on_error(event, *args, **kwargs):
#     if bot.dev:
#         traceback.print_exc()
#     else:
#         embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
#         embed.add_field(name='Event', value=event)
#         embed.description = '```py\n%s\n```' % traceback.format_exc()
#         embed.timestamp = datetime.datetime.utcnow()
#         try:
#             await bot.owner.send(embed=embed)
#         except:
#             pass

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.channel.send(':x: Dieser Command wurde deaktiviert')
    elif isinstance(error, commands.CommandInvokeError):
        if bot.dev:
            raise error
        else:
            embed = discord.Embed(title=':x: Command Error', colour=0x992d22) #Dark Red
            embed.add_field(name='Error', value=error)
            embed.add_field(name='Guild', value=ctx.guild)
            embed.add_field(name='Channel', value=ctx.channel)
            embed.add_field(name='User', value=ctx.author)
            embed.add_field(name='Message', value=ctx.message.clean_content)
            embed.timestamp = datetime.datetime.utcnow()
            try:
                await bot.owner.send(embed=embed)
            except:
                pass

@bot.command(hidden=True, aliases=['quit_backup'])
async def shutdown_backup(ctx):
    '''Fallback if mod cog couldn't load'''
    if await ctx.bot.is_owner(ctx.author):
        await ctx.send('**:ok:** Bye!')
        bot.logout()
        sys.exit(0)
    else:
        await ctx.send('**:no_entry:** Du bist nicht mein Bot Besitzer!')

if __name__ == '__main__':
    bot.run(loadconfig.__token__)
