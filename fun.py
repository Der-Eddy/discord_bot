import discord
from discord.ext import commands
import asyncio

class fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cookie(self):
        '''Keks'''
        await self.bot.say(':cookie:')

    @commands.command()
    async def praise(self):
        '''Praise the Sun'''
        await self.bot.say('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def java(self):
        '''Weil Java != Javscript'''
        await self.bot.say(':interrobang: Meintest du jQuery, Javascript oder Node.js? https://abload.de/img/2016-05-102130191kzpu.png')

    @commands.command()
    async def praise(self):
        '''Praise the Sun'''
        await self.bot.say('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def css(self):
        '''Counter Strike: Source'''
        await self.bot.say('http://i.imgur.com/TgPKFTz.gif')

    @commands.command(pass_context=True)
    async def countdown(self, ctx):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await self.bot.say(':{0}:'.format(num))
            await self.bot.send_typing(ctx.message.channel)
            await asyncio.sleep(1)
        await self.bot.say(':ok: DING DING DING')

    @commands.command(pass_context=True)
    async def steinigt(self, ctx, *member:str):
        '''Monty Python'''
        await self.bot.say(member + '\nhttps://media.giphy.com/media/l41lGAcThnMc29u2Q/giphy.gif')

def setup(bot):
    bot.add_cog(fun(bot))
