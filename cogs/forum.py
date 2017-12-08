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
        self.discourseURL = 'https://www.kokoro-ko.de'

    async def __error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @staticmethod
    async def _getDiscordTag(username, userAgentHeaders):
        if username.startswith('https://www.elitepvpers.com/forum/'):
            url = username
        else:
            url = f'https://www.elitepvpers.com/forum/member.php?username={username}'
        async with aiohttp.ClientSession(cookies = loadconfig.__cookieJar__, headers = userAgentHeaders) as cs:
            async with cs.get(url) as r:
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
    @commands.cooldown(1, 5, commands.cooldowns.BucketType.guild)
    async def epvpis(self, ctx, *user: str):
        '''Search for an username on elitepvpers.com

        Beispiel:
        -----------

        :epvpis Der-Eddy
        '''
        url = 'https://www.elitepvpers.com/forum/ajax.php?do=usersearch'
        payload = {
            'do': 'usersearch',
            'fragment': ' '.join(user)
        }
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data = payload, headers = self.bot.userAgentHeaders) as r:
                root = ET.fromstring(await r.text())
                if len(root) > 0:
                    embed = discord.Embed(color=0xf1c40f) #golden
                    embed.set_footer(text='A maximum of 15 user can be displayed')
                    embed.set_thumbnail(url='https://abload.de/img/epvp_shield_hiresyskb3.png')
                    msg = ':ok: I could find {} user!'.format(len(root))
                    for i in root:
                        userURL = 'https://www.elitepvpers.com/forum/member.php?u=' + i.attrib['userid']
                        embed.add_field(name=i.text, value=userURL, inline=False)
                    await ctx.send(msg, embed=embed)
                else:
                    msg = f':no_entry: Couldn\'t find any user **{username}** :sweat:'
                    await ctx.send(msg)

    # @epvpis.error
    # async def epvpis_error(self, error, ctx):
    #     if isinstance(error, commands.errors.CommandOnCooldown):
    #         seconds = str(error)[34:]
    #         await ctx.send(f':alarm_clock: Cooldown! Try again in {seconds}')

    @commands.command(aliases=['verify'])
    @commands.cooldown(1, 5, commands.cooldowns.BucketType.guild)
    async def epvpverify(self, ctx, *user: str):
        '''Verifying a discord user via elitepvpers

        Beispiel:
        -----------

        :epvpverify

        :epvpverify Der-Eddy

        :verify https://www.elitepvpers.com/forum/members/984054-der-eddy.html
        '''
        #Eddys Server
        if ctx.message.guild.id == 102817255661772800:
            verifyRole = 'Member'
        #Coding Lounge
        elif ctx.message.guild.id == 161637499939192832:
            verifyRole = 'Verified Account'
        else:
            await ctx.send('**:no_entry:** This command only works on some selected servers!')
            return

        role = discord.utils.get(ctx.guild.roles, name=verifyRole)

        if len(user) == 0:
            username = ctx.author.name
        else:
            if user[0] == 'remove':
                try:
                    await ctx.author.remove_roles(role)
                    await ctx.send(f':ok: Role **{role}** removed')
                except:
                    pass
                finally:
                    return
            else:
                username = ' '.join(user)
        tmp = await ctx.send(f':ok: Trying to verify Discord user **{ctx.author}** with Elitepvpers user **{username}**...')
        async with ctx.channel.typing():
            if str(ctx.author) == await self._getDiscordTag(username, self.bot.userAgentHeaders):
                if role in ctx.message.author.roles:
                    await tmp.edit(content = f':negative_squared_cross_mark: You already have the role **{role}**!')
                else:
                    try:
                        await ctx.author.add_roles(role)
                        if not username.startswith('https://www.elitepvpers.com/forum/'):
                            await ctx.author.edit(nick = username)
                    except:
                        pass
                    await tmp.edit(content = f':white_check_mark: User **{username}** successfully verified! Added to role **{role}**')
            else:
                await tmp.edit(content = f':x: Could not verify Discord user **{ctx.author}** with Elitepvpers user **{username}**')
                await ctx.author.send('I\'m messaging you because I couldn\'t verify you with your corresponding Elitepvpers account' +
                                       '\n\nYou will need to specify your Elitepvpers username with the `:verify` command in case your Discord username is' +
                                       '**not** the same as your Elitepvpers username.' +
                                       'This can be done via `:verify [YOUR ELITEPVPERS USERNAME]`' +
                                       '\n\nAlso don\'t forget to add your Discord username + discriminator in your elitepvpers settings! ' +
                                       '(<https://www.elitepvpers.com/forum/profile.php?do=editprofile>) \nhttps://i.imgur.com/4ckQsjX.png')

    # @epvpverify.error
    # async def epvpverify_error(self, error, ctx):
    #     if isinstance(error, commands.errors.CommandOnCooldown):
    #         await ctx.send(str(error))
    #     else:
    #         await ctx.send('Having currently difficulties to reach elitepvpers. Try it again in some hours.')

    # @commands.command(aliases=['user'])
    # @commands.cooldown(2, 1, commands.cooldowns.BucketType.guild)
    # async def kokoro(self, ctx, *user: str):
    #     '''Gibt Benutzerdaten über einen Benutzer aus Kokoro-ko.de aus
    #
    #     Beispiel:
    #     -----------
    #
    #     :kokoro
    #
    #     :user Eddy
    #     '''
    #     if len(user) == 0:
    #         username = ctx.author.name
    #     else:
    #         username = user[0]
    #
    #     url = f'{self.discourseURL}/users/{username}.json'
    #     async with aiohttp.ClientSession() as cs:
    #         async with cs.put(url, data = loadconfig.__discourseAPIKey__) as r:
    #             json = await r.json()
    #             if json['user']['primary_group_flair_bg_color'] == None or True:
    #                 color = 0xff6600 #orange
    #             else:
    #                 #color = hex(int(json['user']['primary_group_flair_bg_color'], 16))
    #                 color = discord.Color(hex(int(json['user']['primary_group_flair_bg_color'], 16)))
    #                 print(color.value)
    #                 #currently not working??
    #             embed = discord.Embed(color=color)
    #             embed.set_footer(text='kokoro-ko.de - Dein Anime und Gaming forum')
    #             avatarURL = self.discourseURL + json['user']['avatar_template']
    #             embed.set_thumbnail(url=avatarURL.format(size = '124'))
    #             if json['user']['name'] == '':
    #                 discordName = json['user']['username']
    #             else:
    #                 discordName = '{} ({})'.format(json['user']['username'], json['user']['name'])
    #             embed.add_field(name='Username', value=discordName, inline=True)
    #             embed.add_field(name='Vertrauensstufe', value=json['user']['trust_level'], inline=True)
    #             if json['user']['title'] != '' and json['user']['title'] != None:
    #                 embed.add_field(name='Titel', value=json['user']['title'], inline=True)
    #             embed.add_field(name='Registriert am', value=json['user']['created_at'], inline=True)
    #             embed.add_field(name='Abzeichen', value=json['user']['badge_count'], inline=True)
    #             embed.add_field(name='Beiträge', value=json['user']['post_count'], inline=True)
    #             if json['user']['user_fields']['7'] != '' and json['user']['user_fields']['7'] != None:
    #                 embed.add_field(name='Discord', value=json['user']['user_fields']['7'], inline=True)
    #             if json['user']['user_fields']['1'] != '' and json['user']['user_fields']['1'] != None:
    #                 embed.add_field(name='Steam', value='http://steamcommunity.com/id/' + json['user']['user_fields']['1'], inline=True)
    #             groups = ''
    #             for group in json['user']['groups']:
    #                 if group['automatic'] == False:
    #                     groups += group['name'] + ', '
    #             if groups != '':
    #                 embed.add_field(name='Gruppen', value=groups[:-2], inline=True)
    #             embed.add_field(name='Profile Link', value=f'{self.discourseURL}/users/{username}/summary', inline=True)
    #             await ctx.send(embed=embed)
    #         else:
    #             msg = f':no_entry: Ich konnte keinen Account **{username}** auf kokoro-ko.de finden :sweat:'
    #             await ctx.send(msg)

    # @kokoro.error
    # async def kokoro_error(self, error, ctx):
    #     if isinstance(error, commands.errors.CommandOnCooldown):
    #         seconds = str(error)[34:]
    #         await ctx.send(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut')

def setup(bot):
    bot.add_cog(forum(bot))
