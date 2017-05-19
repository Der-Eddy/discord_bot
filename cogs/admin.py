import sys
import discord
from discord.ext import commands
from memory_profiler import profile, memory_usage
import loadconfig
import checks

class admin():
    '''Befehle für den Bot Admin'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['quit'], hidden=True)
    @checks.is_bot_owner()
    async def shutdown(self, ctx):
        '''Schaltet mich ab :( (BOT OWNER ONLY)'''
        await self.bot.say('**:ok:** Bye!')
        #self.bot.gamesLoop.cancel()
        self.bot.logout()
        sys.exit(0)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def avatar(self, ctx, url: str):
        '''Setzt einen neuen Avatar (BOT OWNER ONLY)'''
        tempAvaFile = 'tempAva.png'
        async with aiohttp.get(''.join(url)) as img:
            with open(tempAvaFile, 'wb') as f:
                f.write(await img.read())
        with open(tempAvaFile, 'rb') as f:
            await self.bot.edit_profile(avatar=f.read())
        os.remove(tempAvaFile)
        asyncio.sleep(2)
        await self.bot.say('**:ok:** Mein neuer Avatar!\n %s' % self.bot.user.avatar_url)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def game(self, ctx, *, gameName: str):
        '''Ändert das derzeit spielende Spiel (BOT OWNER ONLY)'''
        await self.bot.change_presence(game=discord.Game(name=gameName))
        await self.bot.say(f'**:ok:** Ändere das Spiel zu: Playing **{gameName}**')

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def name(self, ctx, name: str):
        '''Ändert den globalen Namen vom Bot (BOT OWNER ONLY)'''
        await self.bot.edit_profile(username=name)
        msg = ':ok: Ändere meinen Namen zu: **{0}**'.format(name)
        await self.bot.say(msg)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def servers(self, ctx):
        '''Listet die aktuellen verbundenen Server auf (BOT OWNER ONLY)'''
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>4s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for server in self.bot.servers:
            msg += '{!s:19s} | {!s:>4s}| {} | {}\n'.format(server.id, server.member_count, server.name, server.owner)
        msg += '```'
        await self.bot.say(msg)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def leaveserver(self, ctx, serverid: str):
        '''Tritt aus einem Server aus (BOT OWNER ONLY)

        Beispiel:
        -----------

        :leaveserver 102817255661772800
        '''
        server = self.bot.get_server(serverid)
        if server:
            await self.bot.leave_server(server)
            msg = ':ok: Austritt aus {} erfolgreich!'.format(server.name)
        else:
            msg = ':x: Konnte keinen passenden Server zu dieser ID finden!'
        await self.bot.say(msg)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def echo(self, ctx, channel: str, *message: str):
        '''Gibt eine Nachricht als Bot auf einem bestimmten Channel aus (BOT OWNER ONLY)'''
        ch = self.bot.get_channel(channel)
        msg = ' '.join(message)
        await self.bot.send_message(ch, msg)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def discriminator(self, ctx, disc: str):
        '''Gibt Benutzer mit dem jeweiljigen Discriminator zurück'''

        discriminator = disc
        memberList = ''

        for server in self.bot.servers:
            for member in server.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await self.bot.say(memberList)
        else:
            await self.bot.say(':x: Konnte niemanden finden')

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def test(self, ctx):
        '''Test Test Test'''

        #bReturn = self.bot.gamesLoop.cancel()
        #await self.bot.say(bReturn)

        #mem_usage = memory_usage(-1)
        #await self.bot.say(mem_usage)
        await self.bot.say('<:faeSad:298772756127023104>')

def setup(bot):
    bot.add_cog(admin(bot))
