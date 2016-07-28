import discord
from discord.ext import commands
import sys
import asyncio
import aiohttp
import random

try:
    from config import __token__, __prefix__, __game__, __adminid__, __adminrole__, __kawaiichannel__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __game__ = os.environ.get('DISCORD_GAME')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __adminrole__ = os.environ.get('DISCORD_ADMINROLE')
    __kawaiichannel__ = os.environ.get('DISCORD_KAWAIICHANNEL')

class anime():
    '''Alles rund um Animes'''
    kawaiich = __kawaiichannel__

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kawaii(self, ctx):
        '''Gibt ein random kawaii Bild aus'''
        if self.kawaiich:
            pins = await self.bot.pins_from(self.bot.get_channel(self.kawaiich))
            rnd = random.choice(pins)
            img = rnd.attachments[0]['url']
            await self.bot.say('Von: {0}: {1}'.format(rnd.author, img))
        else:
            await self.bot.say(':no_entry: Es wurde kein Channel für den Bot eingestellt! Wende dich bitte an den Bot Admin')

def setup(bot):
    bot.add_cog(anime(bot))
