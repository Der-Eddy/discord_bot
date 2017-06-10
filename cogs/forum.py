import sys
import random
import re
import asyncio
import xml.etree.ElementTree as ET
import aiohttp
import discord
from discord.ext import commands
import loadconfig

class forum():
    '''Forum spezifische Commands'''

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def _getDiscordTag(username, userAgentHeaders):
        url = f'https://www.elitepvpers.com/forum/member.php?username={username}'
        async with aiohttp.get(url, cookies=loadconfig.__cookieJar__, headers = userAgentHeaders) as r:
            if r.status == 200:
                content = await r.text()
                #with open('debug.html', 'w', encoding='utf-8') as file_:
                #    file_.write(content)
                regex = r"<dt class=\"shade\">Discord<\/dt>\n<dd>(?P<username>.+)#(?P<discriminator>\d{4})<\/dd>"
                match = re.search(regex, content)
                try:
                    return match.group(1) + '#' + match.group(2)
                except AttributeError:
                    return ''

    @commands.command(aliases=['epvp'])
    async def epvpis(self, user: str):
        '''Sucht nach einem Benutzernamen auf Elitepvpers

        Beispiel:
        -----------

        :epvpis Der-Eddy
        '''
        url = 'https://www.elitepvpers.com/forum/ajax.php?do=usersearch'
        payload = {
            'do': 'usersearch',
            'fragment': user
        }
        async with aiohttp.post(url, data=payload, headers = self.bot.userAgentHeaders) as r:
            if r.status == 200:
                root = ET.fromstring(await r.text())
                if len(root) > 0:
                    embed = discord.Embed(color=0xf1c40f) #golden
                    embed.set_footer(text='Es können maximal 15 Accounts gefunden werden')
                    embed.set_thumbnail(url='https://abload.de/img/epvp_shield_hiresyskb3.png')
                    msg = ':ok: Ich konnte {} Accounts finden!'.format(len(root))
                    for i in root:
                        userURL = 'https://www.elitepvpers.com/forum/member.php?u=' + i.attrib['userid']
                        embed.add_field(name=i.text, value=userURL, inline=False)
                    await self.bot.say(msg, embed=embed)
                else:
                    msg = ':no_entry: Ich konnte keine Epvp Accounts finden :sweat:'
                    await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['verify'])
    async def epvpverify(self, ctx, *user: str):
        '''Verifying a discord user via elitepvpers

        Beispiel:
        -----------

        :epvpverify

        :epvpverify Der-Eddy
        '''
        #Eddys Server
        if ctx.message.server.id == '102817255661772800':
            verifyRole = 'Member'
        #Coding Channel
        elif ctx.message.server.id == '161637499939192832':
            verifyRole = 'Verified Account'
        else:
            await self.bot.say('**:no_entry:** This command only works on some selected servers!')
            return

        if len(user) == 0:
            username = ctx.message.author.name
        else:
            username = user[0]
        tmp = await self.bot.say(f':ok: Trying to verify Discord user **{ctx.message.author}** with Elitepvpers user **{username}**...')
        await self.bot.send_typing(ctx.message.channel)

        if str(ctx.message.author) == await self._getDiscordTag(username, self.bot.userAgentHeaders):
            role = discord.utils.get(ctx.message.server.roles, name=verifyRole)
            if role in ctx.message.author.roles:
                try:
                    await self.bot.remove_roles(ctx.message.author, role)
                except:
                    pass
                await self.bot.edit_message(tmp, f':negative_squared_cross_mark: Role **{role}** removed')
            else:
                try:
                    await self.bot.add_roles(ctx.message.author, role)
                except:
                    pass
                await self.bot.edit_message(tmp, f':white_check_mark: User **{username}** successfully verified! Added to role **{role}**')
        else:
            await self.bot.edit_message(tmp, f':x: Could not verify user **{username}**')
            await self.bot.send_message(ctx.message.author, 'I\'m messaging you because I couldn\'t verify you with your corresponding Elitepvpers account' +
                                   '\n\nYou will need to specify your Elitepvpers username with the `:verify` command in case your Discord username is' +
                                   '**not** the same as your Elitepvpers username.' +
                                   'This can be done via `:verify [YOUR ELITEPVPERS USERNAME]`' +
                                   '\n\nAlso don\'t forget to add your Discord username + discriminator in your elitepvpers settings! ' +
                                   '(<https://www.elitepvpers.com/forum/profile.php?do=editprofile>) \nhttps://i.imgur.com/4ckQsjX.png')

def setup(bot):
    bot.add_cog(forum(bot))
