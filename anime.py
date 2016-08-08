import discord
from discord.ext import commands
import sys
import asyncio
import aiohttp
import random

try:
    from config import __token__, __prefix__, __adminid__, __adminrole__, __modrole__, __kawaiichannel__, __botlogchannel__, __github__, __botserverid__, __greetmsg__
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

class anime():
    '''Alles rund um Animes'''
    kawaiich = __kawaiichannel__

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kawaii(self, ctx):
        '''Gibt ein zufälliges kawaii Bild aus'''
        if self.kawaiich:
            pins = await self.bot.pins_from(self.bot.get_channel(self.kawaiich))
            rnd = random.choice(pins)
            try:
                img = rnd.attachments[0]['url']
            except IndexError:
                img = rnd.content
            emojis = [':blush:', ':flushed:', ':heart_eyes:', ':heart_eyes_cat:', ':heart:']
            await self.bot.say('{2} Von: {0}: {1}'.format(rnd.author.display_name, img, random.choice(emojis)))
        else:
            await self.bot.say('**:no_entry:** Es wurde kein Channel für den Bot eingestellt! Wende dich bitte an den Bot Admin')

def setup(bot):
    bot.add_cog(anime(bot))
