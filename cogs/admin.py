import sys
import os
import random
import discord
import asyncio
import aiohttp
from discord.ext import commands
import loadconfig

class admin(commands.Cog):
    '''Befehle für den Bot Admin'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    @commands.command(aliases=['quit'], hidden=True)
    async def shutdown(self, ctx):
        '''Schaltet mich ab :( (BOT OWNER ONLY)'''
        await ctx.send('**:ok:** Bye!')
        #self.bot.gamesLoop.cancel()
        await self.bot.logout()
        sys.exit(0)

    @commands.command(hidden=True)
    async def restart(self, ctx):
        '''Startet mich neu (BOT OWNER ONLY)'''
        await ctx.send('**:ok:** Bis gleich!')
        await self.bot.logout()
        sys.exit(6)

    @commands.command(hidden=True)
    async def avatar(self, ctx, url: str):
        '''Setzt einen neuen Avatar (BOT OWNER ONLY)'''
        tempAvaFile = 'tempAva.png'
        async with aiohttp.get(''.join(url)) as img:
            with open(tempAvaFile, 'wb') as f:
                f.write(await img.read())
        f = discord.File(tempAvaFile)
        await self.bot.edit_profile(avatar=f.read())
        os.remove(tempAvaFile)
        asyncio.sleep(2)
        await ctx.send('**:ok:** Mein neuer Avatar!\n %s' % self.bot.user.avatar_url)

    @commands.command(hidden=True, aliases=['game'])
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        '''Ändert das derzeit spielende Spiel (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            type = discord.Activity.playing
        elif gameType == 'watching':
            type = discord.Activity.watching
        elif gameType == 'listening':
            type = discord.Activity.listening
        elif gameType == 'streaming':
            type = discord.Activity.streaming
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(activity=discord.Activity(type=type, name=gameName))
        await ctx.send(f'**:ok:** Ändere das Spiel zu: {gameType} **{gameName}**')

    @commands.command(hidden=True)
    async def changestatus(self, ctx, status: str):
        '''Ändert den Online Status vom Bot (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)
        await ctx.send(f'**:ok:** Ändere Status zu: **{discordStatus}**')

    @commands.command(hidden=True)
    async def name(self, ctx, name: str):
        '''Ändert den globalen Namen vom Bot (BOT OWNER ONLY)'''
        await self.bot.edit_profile(username=name)
        msg = f':ok: Ändere meinen Namen zu: **{name}**'
        await ctx.send(msg)

    @commands.command(hidden=True, aliases=['guilds'])
    async def servers(self, ctx):
        '''Listet die aktuellen verbundenen Guilds auf (BOT OWNER ONLY)'''
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def leaveserver(self, ctx, guildid: str):
        '''Tritt aus einem Server aus (BOT OWNER ONLY)

        Beispiel:
        -----------

        :leaveserver 102817255661772800
        '''
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f':ok: Austritt aus {guild.name} erfolgreich!'
            else:
                msg = ':x: Konnte keine passende Guild zu dieser ID finden!'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def echo(self, ctx, channel: str, *message: str):
        '''Gibt eine Nachricht als Bot auf einem bestimmten Channel aus (BOT OWNER ONLY)'''
        ch = self.bot.get_channel(int(channel))
        msg = ' '.join(message)
        await ch.send(msg)
        await ctx.message.delete()

    @commands.command(hidden=True)
    async def discriminator(self, ctx, disc: str):
        '''Gibt Benutzer mit dem jeweiligen Discriminator zurück'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(':x: Konnte niemanden finden')

    @commands.command(hidden=True)
    @commands.bot_has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, *name):
        '''Ändert den Server Nickname vom Bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Ändere meinen Server Nickname zu: **{nickname}**'
        else:
            msg = f':ok: Reset von meinem Server Nickname auf: **{ctx.me.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, member: discord.Member=None, *name):
        '''Ändert den Nickname eines Benutzer (BOT OWNER ONLY)'''
        if member == None:
            member = ctx.author
        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f':ok: Ändere Nickname von {member} zu: **{nickname}**'
        else:
            msg = f':ok: Reset von Nickname für {member} auf: **{member.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def geninvite(self, ctx, serverid: str):
        '''Generiert einen Invite für eine Guild wenn möglich (BOT OWNER ONLY)'''
        guild = self.bot.get_guild(int(serverid))
        invite = await self.bot.create_invite(guild, max_uses=1, unique=False)
        msg = f'Invite für **{guild.name}** ({guild.id})\n{invite.url}'
        await ctx.author.send(msg)

    @commands.command(hidden=True, aliases=['wichteln'])
    async def wichtel(self, ctx, *participants: str):
        '''Nützlich für das Community Wichtel Event 2018 (BOT OWNER ONLY)'''
        participantsList = list(participants)
        random.shuffle(participantsList)
        msg = 'Wichtelpartner stehen fest:\n```'
        for i, val in enumerate(participantsList):
            if i == len(participantsList) - 1:
                msg += f'{val.ljust(10)} ===> {participantsList[0]}\n'
            else:
                msg += f'{val.ljust(10)} ===> {participantsList[i + 1]}\n'

        msg += '```'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.channel)
    async def test(self, ctx):
        '''Test Test Test'''
        await ctx.send('Test')
        await self.bot.AppInfo.owner.send('Test')
        await ctx.send(self.bot.cogs)

def setup(bot):
    bot.add_cog(admin(bot))
