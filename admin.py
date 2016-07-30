import discord
from discord.ext import commands
import sys
import asyncio

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

class admin():
    '''Praktische Befehle für Administratoren'''
    admin = __adminrole__
    owner = __adminid__

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
        '''Schaltet mich ab :( (OWNER ONLY)'''
        if ctx.message.author.id == self.owner:
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
    async def purge(self, ctx, *limit):
        '''Löscht mehere Nachrichten auf einmal'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            limit = int(limit[0])
            deleted = 0
            while limit > 1:
                cap = min(limit, 100)
                deleted += len(await self.bot.purge_from(ctx.message.channel, limit=cap, before=ctx.message))
                limit -= cap
            tmp = await self.bot.send_message(ctx.message.channel, ':put_litter_in_its_place: {0} Nachrichten gelöscht'.format(deleted))
            await self.bot.delete_message(ctx.message)
            await asyncio.sleep(3)
            await self.bot.delete_message(tmp)

    @commands.command(pass_context=True)
    async def nickname(self, ctx, *name):
        '''Ändert den Nickname vom Bot'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            nickname = ' '.join(name)
            await self.bot.change_nickname(ctx.message.server.get_member(self.bot.user.id), nickname)
            if nickname:
                msg = ':ok: Ändere meinen Namen zu: **{0}**'.format(nickname)
            else:
                msg = ':ok: Reset von meinem Nickname auf: **{0}**'.format(self.bot.user.name)
        else:
            msg = ':no_entry: Du hast nicht die Rolle {0}!'.format(self.admin)
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(admin(bot))
