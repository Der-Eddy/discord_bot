import discord
from discord.ext import commands
import sys
import asyncio
import datetime
from pytz import timezone

try:
    from config import __token__, __prefix__, __adminid__, __adminrole__, __modrole__, __kawaiichannel__, __botlogchannel__, __github__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __adminrole__ = os.environ.get('DISCORD_ADMINROLE')
    __modrole__ = os.environ.get('DISCORD_MODROLE')
    __kawaiichannel__ = os.environ.get('DISCORD_KAWAIICHANNEL')
    __botlogchannel__ = os.environ.get('DISCORD_BOTLOGCHANNEL')
    __github__ = os.environ.get('DISCORD_GITHUB')

class admin():
    '''Praktische Befehle für Administratoren und Moderatoren'''
    admin = __adminrole__
    mod = __modrole__
    owner = __adminid__

    def __init__(self, bot):
        self.bot = bot

    def _currenttime(self):
        return datetime.datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")

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
            await self.bot.say('**:ok:** Bye!')
            self.bot.logout()
            sys.exit(0)
        else:
            await self.bot.say('**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.admin))

    @commands.command(pass_context=True)
    async def game(self, ctx, *game):
        '''Ändert das derzeit spielende Spiel (ADMIN ONLY)'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            gameName = ' '.join(game)
            await self.bot.change_status(game=discord.Game(name=gameName))
            await self.bot.say('**:ok:** Ändere das Spiel zu: Playing **{0}**'.format(gameName))
        else:
            await self.bot.say('**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.admin))

    @commands.command(pass_context=True)
    async def purge(self, ctx, *limit):
        '''Löscht mehere Nachrichten auf einmal (ADMIN ONLY)'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            limit = int(limit[0])
            deleted = 0
            while limit > 1:
                cap = min(limit, 100)
                deleted += len(await self.bot.purge_from(ctx.message.channel, limit=cap, before=ctx.message))
                limit -= cap
            tmp = await self.bot.send_message(ctx.message.channel, '**:put_litter_in_its_place:** {0} Nachrichten gelöscht'.format(deleted))
            await self.bot.delete_message(ctx.message)
            await asyncio.sleep(3)
            await self.bot.delete_message(tmp)

    @commands.command(pass_context=True)
    async def nickname(self, ctx, *name):
        '''Ändert den Nickname vom Bot (ADMIN ONLY)'''
        author = ctx.message.author
        if self.checkRole(author, self.admin):
            nickname = ' '.join(name)
            await self.bot.change_nickname(ctx.message.server.get_member(self.bot.user.id), nickname)
            if nickname:
                msg = ':ok: Ändere meinen Namen zu: **{0}**'.format(nickname)
            else:
                msg = ':ok: Reset von meinem Nickname auf: **{0}**'.format(self.bot.user.name)
        else:
            msg = '**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.admin)
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def kick(self, ctx, member: discord.Member = None, *reason):
        '''Kickt ein Mitglied mit einer Begründung (MOD ONLY)'''
        author = ctx.message.author
        if self.checkRole(author, self.mod):
            if member is not None:
                if reason:
                    reason = ' '.join(reason)
                else:
                    reason = 'None'
                memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
                await self.bot.send_message(self.bot.get_channel(__botlogchannel__), '`[{0}]` **:passport_control:** {1} wurde gekickt vom Server {2} von {3}\n **Begründung:**```{4}```'.format(self._currenttime(), memberExtra, member.server, ctx.message.author, reason))
                await self.bot.kick(member)
            else:
                tmp = await self.bot.say('**:no_entry:** Du musst einen Benutzer spezifizieren!')
                await asyncio.sleep(5)
                await self.bot.delete_message(tmp)
        else:
            tmp = await self.bot.say('**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.mod))
            await asyncio.sleep(5)
            await self.bot.delete_message(tmp)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def ban(self, ctx, member: discord.Member = None, *reason):
        '''Bannt ein Mitglied mit einer Begründung (MOD ONLY)'''
        author = ctx.message.author
        if self.checkRole(author, self.mod):
            if member is not None:
                if reason:
                    reason = ' '.join(reason)
                else:
                    reason = 'None'
                memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
                await self.bot.send_message(self.bot.get_channel(__botlogchannel__), '`[{0}]` **:customs:** {1} wurde gebannt vom Server {2} von {3}\n **Begründung:**```{4}```'.format(self._currenttime(), memberExtra, member.server, ctx.message.author, reason))
                await self.bot.ban(member)
            else:
                tmp = await self.bot.say('**:no_entry:** Du musst einen Benutzer spezifizieren!')
                await asyncio.sleep(5)
                await self.bot.delete_message(tmp)
        else:
            tmp = await self.bot.say('**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.mod))
            await asyncio.sleep(5)
            await self.bot.delete_message(tmp)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def unban(self, ctx, user: int = None, *reason):
        '''Entbannt ein Mitglied mit einer Begründung (MOD ONLY)'''
        author = ctx.message.author
        user = discord.User(id=user)
        if self.checkRole(author, self.mod):
            if user is not None:
                if reason:
                    reason = ' '.join(reason)
                else:
                    reason = 'None'
                memberExtra = '{0} - *{1} ({2})*'.format(user.mention, user, user.id)
                await self.bot.send_message(self.bot.get_channel(__botlogchannel__), '`[{0}]` **:negative_squared_cross_mark:** {1} wurde entbannt vom Server {2} von {3}\n **Begründung:**```{4}```'.format(self._currenttime(), memberExtra, ctx.message.server, ctx.message.author, reason))
                await self.bot.unban(ctx.message.server, user)
            else:
                tmp = await self.bot.say('**:no_entry:** Du musst einen Benutzer spezifizieren!')
                await asyncio.sleep(5)
                await self.bot.delete_message(tmp)
        else:
            tmp = await self.bot.say('**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.mod))
            await asyncio.sleep(5)
            await self.bot.delete_message(tmp)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def bans(self, ctx):
        '''Listet aktuell gebannte User auf (MOD ONLY)'''
        author = ctx.message.author
        if self.checkRole(author, self.mod):
            user = await self.bot.get_bans(ctx.message.server)
            if len(user) > 0:
                msg = ''
                for u in user:
                    msg += 'User: {0} - ID: {1}\n'.format(u, u.id)
                await self.bot.say(msg)
            else:
                await self.bot.say('**:negative_squared_cross_mark:** Es gibt keine gebannten Nutzer!')
        else:
            tmp = await self.bot.say('**:no_entry:** Du hast nicht die Rolle {0}!'.format(self.mod))
            await asyncio.sleep(5)
            await self.bot.delete_message(tmp)
            await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(admin(bot))
