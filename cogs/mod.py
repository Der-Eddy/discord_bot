import datetime
import asyncio
import aiohttp
import discord
from discord.ext import commands
from pytz import timezone
import loadconfig

class mod():
    '''Praktische Befehle für Administratoren und Moderatoren'''

    def __init__(self, bot):
        self.bot = bot

    def _currenttime(self):
        return datetime.datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")

    @commands.command(aliases=['prune'], hidden=True)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def purge(self, ctx, *limit):
        '''Löscht mehere Nachrichten auf einmal (MOD ONLY)

        Beispiel:
        -----------

        :purge 100
        '''
        try:
            limit = int(limit[0])
        except IndexError:
            limit = 1
        deleted = 0
        while limit >= 1:
            cap = min(limit, 100)
            deleted += len(await ctx.channel.purge(limit=cap, before=ctx.message))
            limit -= cap
        tmp = await ctx.send(f'**:put_litter_in_its_place:** {deleted} Nachrichten gelöscht')
        await asyncio.sleep(15)
        await tmp.delete()
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member = None, *reason):
        '''Kickt ein Mitglied mit einer Begründung (MOD ONLY)

        Beispiel:
        -----------

        :kick @Der-Eddy#6508
        '''
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.kick(reason=reason)
        else:
            await ctx.send('**:no_entry:** Kein Benutzer angegeben!')

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
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
                reason = None
            await member.ban(reason=reason)
        else:
            await ctx.send('**:no_entry:** Kein Benutzer angegeben!')

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
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
                reason = None
            await ctx.guild.unban(user, reason=reason)
        else:
            await ctx.send('**:no_entry:** Kein Benutzer angegeben!')

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def bans(self, ctx):
        '''Listet aktuell gebannte User auf (MOD ONLY)'''
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID":21}{"Name":25} Begründung\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName #:robot: emoji
                reason = str(entry.reason) #Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c) #Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:negative_squared_cross_mark:** Es gibt keine gebannten Nutzer!')

    @commands.command(alias=['clearreactions'], hidden=True)
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def removereactions(self, ctx, messageid : str):
        '''Entfernt alle Emoji Reactions von einer Nachricht (MOD ONLY)

        Beispiel:
        -----------

        :removereactions 247386709505867776
        '''
        message = await ctx.channel.get_message(messageid)
        if message:
            await message.clear_reactions()
        else:
            await ctx.send('**:x:** Konnte keine Nachricht mit dieser ID finden!')

    @commands.command(hidden=True)
    async def permissions(self, ctx):
        '''Listet alle Rechte des Bots auf'''
        permissions = ctx.channel.permissions_for(ctx.me)

        embed = discord.Embed(title=':customs:  Permissions', color=0x3498db) #Blue
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool == True:
                value = ':white_check_mark:'
            else:
                value = ':x:'
            embed.add_field(name=item, value=value)

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def hierarchy(self, ctx):
        '''Listet die Rollen-Hierarchie des derzeitigen Servers auf'''
        msg = f'Rollen-Hierarchie für Server **{ctx.guild}**:\n\n'
        roleDict = {}

        for role in ctx.guild.roles:
            if role.is_default():
                roleDict[role.position] = 'everyone'
            else:
                roleDict[role.position] = role.name

        for role in sorted(roleDict.items(), reverse=True):
            msg += role[1] + '\n'
        await ctx.send(msg)

    @commands.command(hidden=True, alies=['setrole', 'sr'])
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def setrank(self, ctx, member: discord.Member=None, *rankName: str):
        '''Vergibt einen Rang an einem Benutzer

        Beispiel:
        -----------

        :setrole @Der-Eddy#6508 Member
        '''
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.add_roles(rank)
            await ctx.send(f':white_check_mark: Rolle **{rank.name}** wurde an **{member.name}** verteilt')
        else:
            await ctx.send(':no_entry: Du musst einen Benutzer angeben!')

    @commands.command(pass_context=True, hidden=True, alies=['rmrole', 'removerole', 'removerank'])
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def rmrank(self, ctx, member: discord.Member=None, *rankName: str):
        '''Entfernt einen Rang von einem Benutzer

        Beispiel:
        -----------

        :rmrole @Der-Eddy#6508 Member
        '''
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.remove_roles(rank)
            await ctx.send(f':white_check_mark: Rolle **{rank.name}** wurde von **{member.name}** entfernt')
        else:
            await ctx.send(':no_entry: Du musst einen Benutzer angeben!')


def setup(bot):
    bot.add_cog(mod(bot))
