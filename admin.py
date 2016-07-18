import discord
from discord.ext import commands
import sys

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

class admin():
    '''Praktische Befehle für Administratoren'''
    admin = __adminrole__

    def __init__(self, bot):
        self.bot = bot

    def checkRole(self, user, roleRec):
        ok = False
        for all in list(user.roles):
            if all.name == roleRec:
                ok = True
        return ok

    @commands.command(pass_context=True)
    async def shutdown(self, ctx):
        '''Schaltet mich ab :('''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            await self.bot.say(':ok: Bye!')
            self.bot.logout()
            sys.exit(0)
        else:
            await self.bot.say(':no_entry: Du hast nicht die Rolle {0}!'.format(self.admin))

    @commands.command(pass_context=True)
    async def game(self, ctx, *game):
        '''Ändert das derzeit spielende Spiel'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            gameName = ' '.join(game)
            await self.bot.change_status(game=discord.Game(name=gameName))
            await self.bot.say(':ok: Ändere das Spiel zu: Playing **{0}**'.format(gameName))
        else:
            await self.bot.say(':no_entry: Du hast nicht die Rolle {0}!'.format(self.admin))

    @commands.command(pass_context=True)
    async def nickname(self, ctx, *name):
        '''Ändert den Nickname vom Bot FUNZT ATM NICHT'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            nickname = ' '.join(name)
            await self.bot.change_nickname(self.bot.user.id, nickname)
            await self.bot.say(':ok: Ändere meinen Namen zu: **{0}**'.format(nickname))
        else:
            await self.bot.say(':no_entry: Du hast nicht die Rolle {0}!'.format(self.admin))

def setup(bot):
    bot.add_cog(admin(bot))
