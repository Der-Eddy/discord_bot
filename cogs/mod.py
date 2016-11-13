import sys
import datetime
import asyncio
import aiohttp
import discord
from discord.ext import commands
from pytz import timezone
import loadconfig
import checks

class mod():
    '''Praktische Befehle für Administratoren und Moderatoren'''

    def __init__(self, bot):
        self.bot = bot

    def _currenttime(self):
        return datetime.datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")

    @commands.command(pass_context=True, aliases=['quit'])
    @checks.is_bot_owner()
    async def shutdown(self, ctx):
        '''Schaltet mich ab :( (BOT OWNER ONLY)'''
        await self.bot.say('**:ok:** Bye!')
        self.bot.logout()
        sys.exit(0)

    @commands.command(pass_context=True)
    @checks.is_bot_owner()
    async def avatar(self, ctx, url: str):
        '''Setzt einen neuen Avatar (BOT OWNER ONLY)'''
        async with aiohttp.get(''.join(url)) as img:
            with open('tempAva.png', 'wb') as f:
                f.write(await img.read())
        with open('tempAva.png', 'rb') as f:
            await self.bot.edit_profile(avatar=f.read())
        asyncio.sleep(2)
        await self.bot.say('**:ok:** Mein neuer Avatar!\n %s' % self.bot.user.avatar_url)

    @commands.command(pass_context=True)
    @checks.is_bot_owner()
    async def game(self, ctx, *game):
        '''Ändert das derzeit spielende Spiel (BOT OWNER ONLY)'''
        gameName = ' '.join(game)
        await self.bot.change_presence(game=discord.Game(name=gameName))
        await self.bot.say('**:ok:** Ändere das Spiel zu: Playing **{0}**'.format(gameName))

    @commands.command(pass_context=True, aliases=['prune'])
    @checks.has_permissions('ban_members') # Security Reasons
    async def purge(self, ctx, *limit):
        '''Löscht mehere Nachrichten auf einmal (ADMIN ONLY)

        Beispiel:
        -----------

        :purge 100
        '''
        try:
            limit = int(limit[0])
        except IndexError:
            limit = 1
        deleted = 0
        while limit > 1:
            cap = min(limit, 100)
            deleted += len(await self.bot.purge_from(ctx.message.channel, limit=cap, before=ctx.message))
            limit -= cap
        tmp = await self.bot.send_message(ctx.message.channel, '**:put_litter_in_its_place:** {0} Nachrichten gelöscht'.format(deleted))
        await asyncio.sleep(15)
        await self.bot.delete_message(tmp)


    @commands.command(pass_context=True)
    @checks.is_administrator()
    async def nickname(self, ctx, *name):
        '''Ändert den Server Nickname vom Bot (ADMIN ONLY)'''
        nickname = ' '.join(name)
        await self.bot.change_nickname(ctx.message.server.get_member(self.bot.user.id), nickname)
        if nickname:
            msg = ':ok: Ändere meinen Server Nickname zu: **{0}**'.format(nickname)
        else:
            msg = ':ok: Reset von meinem Server Nickname auf: **{0}**'.format(self.bot.user.name)
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @checks.is_bot_owner()
    async def name(self, ctx, *name):
        '''Ändert den globalen Namen vom Bot (BOT OWNER ONLY)'''
        name = ' '.join(name)
        await self.bot.edit_profile(username=name)
        msg = ':ok: Ändere meinen Namen zu: **{0}**'.format(name)
        await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['k'])
    @checks.has_permissions('kick_members')
    async def kick(self, ctx, member: discord.Member=None, *reason):
        '''Kickt ein Mitglied mit einer Begründung (MOD ONLY)

        Beispiel:
        -----------

        :kick @Der-Eddy#6508
        '''
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = 'None'
            memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
            await self.bot.send_message(self.bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:passport_control:** {1} wurde gekickt vom Server {2} von {3}\n **Begründung:**```{4}```'.format(self._currenttime(), memberExtra, member.server, ctx.message.author, reason))
            await self.bot.kick(member)
        else:
            tmp = await self.bot.say('**:no_entry:** Du musst einen Benutzer angeben!')
            await asyncio.sleep(15)
            await self.bot.delete_message(tmp)

    @commands.command(pass_context=True, aliases=['b'])
    @checks.has_permissions('ban_members')
    async def ban(self, ctx, member: discord.Member=None, *reason):
        '''Bannt ein Mitglied mit einer Begründung (MOD ONLY)

        Beispiel:
        -----------

        :ban @Der-Eddy#6508
        '''
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = 'None'
            memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
            await self.bot.send_message(self.bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:customs:** {1} wurde gebannt vom Server {2} von {3}\n **Begründung:**```{4}```'.format(self._currenttime(), memberExtra, member.server, ctx.message.author, reason))
            await self.bot.ban(member)
        else:
            tmp = await self.bot.say('**:no_entry:** Du musst einen Benutzer spezifizieren!')
            await asyncio.sleep(15)
            await self.bot.delete_message(tmp)

    @commands.command(pass_context=True)
    @checks.has_permissions('ban_members')
    async def unban(self, ctx, user: int=None, *reason):
        '''Entbannt ein Mitglied mit einer Begründung (MOD ONLY)
        Es muss die Benutzer-ID angegeben werden, Name + Discriminator reicht nicht

        Beispiel:
        -----------

        :unban 102815825781596160
        '''
        user = discord.User(id=user)
        if user is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = 'None'
            memberExtra = '{0} - *{1} ({2})*'.format(user.mention, user, user.id)
            await self.bot.send_message(self.bot.get_channel(loadconfig.__botlogchannel__), '`[{0}]` **:negative_squared_cross_mark:** {1} wurde entbannt vom Server {2} von {3}\n **Begründung:**```{4}```'.format(self._currenttime(), memberExtra, ctx.message.server, ctx.message.author, reason))
            await self.bot.unban(ctx.message.server, user)
        else:
            tmp = await self.bot.say('**:no_entry:** Du musst einen Benutzer spezifizieren!')
            await asyncio.sleep(15)
            await self.bot.delete_message(tmp)

    @commands.command(pass_context=True)
    @checks.has_permissions('kick_members')
    async def bans(self, ctx):
        '''Listet aktuell gebannte User auf (MOD ONLY)'''
        users = await self.bot.get_bans(ctx.message.server)
        if len(users) > 0:
            msg = ''
            for user in users:
                msg += 'User: {0} - ID: {1}\n'.format(user, user.id)
            await self.bot.say(msg)
        else:
            await self.bot.say('**:negative_squared_cross_mark:** Es gibt keine gebannten Nutzer!')

def setup(bot):
    bot.add_cog(mod(bot))
