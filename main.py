import logging
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

__version__ = '1.6.2'
description = '''Der-Eddys anime discord bot, developed with discord.py\n
                 A full list of all commands are available here: https://github.com/Der-Eddy/discord_bot#commands-list'''

log = logging.getLogger('discord')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

def _currenttime():
    return datetime.datetime.now(timezone(loadconfig.__timezone__)).strftime('%H:%M:%S')

class ShinobuBot(commands.AutoShardedBot):
    def __init__(self, docker):
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        self.docker = docker
        super().__init__(command_prefix=loadconfig.__prefix__, description=description, intents=intents)

    async def _randomGame(self):
        #Check games.py to change the list of "games" to be played
        while True:
            guildCount = len(self.guilds)
            memberCount = len(list(self.get_all_members()))
            randomGame = random.choice(loadconfig.__games__)
            await self.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds = guildCount, members = memberCount)))
            await asyncio.sleep(loadconfig.__gamesTimer__)

    async def on_ready(self):
        if self.user.id == 701915238488080457:
            self.dev = True
        else:
            self.dev = False

        log.info('Logged in as')
        log.info(f'Bot-Name: {self.user.name} | ID: {self.user.id}')
        log.info(f'Dev Mode: {self.dev} | Docker: {self.docker}')
        log.info(f'Discord Version: {discord.__version__}')
        log.info(f'Bot Version: {__version__}')
        self.AppInfo = await self.application_info()
        log.info(f'Owner: {self.AppInfo.owner}')
        log.info('------')
        for cog in loadconfig.__cogs__:
            try:
                self.load_extension(cog)
            except Exception:
                log.warning(f'Couldn\'t load cog {cog}')
        self.commands_used = Counter()
        self.startTime = time.time()
        self.botVersion = __version__
        self.userAgentHeaders = {'User-Agent': f'linux:shinobu_discordbot:v{__version__} (by Der-Eddy)'}
        self.gamesLoop = asyncio.ensure_future(self._randomGame())

    async def on_command(self, ctx):
        self.commands_used[ctx.command.name] += 1
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
        # log.info(f'{msg.created_at}: {msg.author.name} in {dest}: {msg.content}')

    async def on_message(self, message):
        if message.author.bot or message.author.id in loadconfig.__blacklist__:
            return
        if isinstance(message.channel, discord.DMChannel):
            await message.author.send(':x: Sorry, but I don\'t accept commands through direct messages! Please use the `#bots` channel of your corresponding server!')
            return
        if self.dev and not await self.is_owner(message.author):
            return
        if self.user.mentioned_in(message) and message.mention_everyone is False:
            if 'help' in message.content.lower():
                await message.channel.send('Eine volle Liste aller Commands gibts hier: https://github.com/Der-Eddy/discord_bot#commands-list')
            else:
                await message.add_reaction('👀') # :eyes:
        if 'loli' in message.clean_content.lower():
            await message.add_reaction('🍭') # :lollipop:
        if 'instagram.com' in message.clean_content.lower():
            await message.add_reaction('💩') # :poop:
        await self.process_commands(message)

    async def on_member_join(self, member):
        if member.guild.id == loadconfig.__botserverid__ and not self.dev:
            if member.id in loadconfig.__blacklist__:
                member.kick()
                await self.owner.send(f'Benutzer **{member}** automatisch gekickt')
            if loadconfig.__greetmsg__ != '':
                channel = member.guild.system_channel
                emojis = [':wave:', ':congratulations:', ':wink:', ':new:', ':cool:', ':white_check_mark:', ':tada:']
                await channel.send(loadconfig.__greetmsg__.format(emoji = random.choice(emojis), member = member.mention))

    async def on_member_remove(self, member):
        if member.guild.id == loadconfig.__botserverid__ and not self.dev:
            if loadconfig.__leavemsg__ != '':
                channel = member.guild.system_channel
                await channel.send(loadconfig.__leavemsg__.format(member = member.name))

    async def on_guild_join(self, guild):
        embed = discord.Embed(title=':white_check_mark: Guild hinzugefügt', type='rich', color=0x2ecc71) #Green
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Name', value=guild.name, inline=True)
        embed.add_field(name='ID', value=guild.id, inline=True)
        embed.add_field(name='Besitzer', value=f'{guild.owner} ({guild.owner.id})', inline=True)
        embed.add_field(name='Region', value=guild.region, inline=True)
        embed.add_field(name='Mitglieder', value=guild.member_count, inline=True)
        embed.add_field(name='Erstellt am', value=guild.created_at, inline=True)
        await self.AppInfo.owner.send(embed=embed)

    async def on_guild_remove(self, guild):
        embed = discord.Embed(title=':x: Guild entfernt', type='rich', color=0xe74c3c) #Red
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Name', value=guild.name, inline=True)
        embed.add_field(name='ID', value=guild.id, inline=True)
        embed.add_field(name='Besitzer', value=f'{guild.owner} ({guild.owner.id})', inline=True)
        embed.add_field(name='Region', value=guild.region, inline=True)
        embed.add_field(name='Mitglieder', value=guild.member_count, inline=True)
        embed.add_field(name='Erstellt am', value=guild.created_at, inline=True)
        await self.AppInfo.owner.send(embed=embed)

    async def on_error(self, event, *args, **kwargs):
        if self.dev:
            traceback.print_exc()
        else:
            embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
            embed.add_field(name='Event', value=event)
            embed.description = '```py\n%s\n```' % traceback.format_exc()
            embed.timestamp = datetime.datetime.utcnow()
            try:
                await self.AppInfo.owner.send(embed=embed)
            except:
                pass

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.channel.send(':x: Dieser Command wurde deaktiviert')
        elif isinstance(error, commands.CommandInvokeError):
            if self.dev:
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
                    await self.AppInfo.owner.send(embed=embed)
                except:
                    pass

if __name__ == '__main__':
    sys.argv = ''.join(sys.argv[1:])
    if sys.argv.lower() == 'docker':
        docker = True
    else:
        docker = False
    bot = ShinobuBot(docker)
    bot.run(loadconfig.__token__)
