import discord
from discord.ext import commands
import loadconfig
import checks

class admin():
    '''Befehle für den Bot Admin'''

    def __init__(self, bot):
        self.bot = bot

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
    async def game(self, ctx, gameName: str):
        '''Ändert das derzeit spielende Spiel (BOT OWNER ONLY)'''
        await self.bot.change_presence(game=discord.Game(name=gameName))
        await self.bot.say('**:ok:** Ändere das Spiel zu: Playing **{0}**'.format(gameName))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def name(self, ctx, name: str):
        '''Ändert den globalen Namen vom Bot (BOT OWNER ONLY)'''
        await self.bot.edit_profile(username=name)
        msg = ':ok: Ändere meinen Namen zu: **{0}**'.format(name)
        await self.bot.say(msg)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_bot_owner()
    async def server(self, ctx):
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

def setup(bot):
    bot.add_cog(admin(bot))
