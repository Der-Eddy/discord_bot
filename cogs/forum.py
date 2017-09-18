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
    @commands.cooldown(1, 5, commands.cooldowns.BucketType.server)
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
                    msg = f':no_entry: Ich konnte keine Epvp Accounts zu **{username}** finden :sweat:'
                    await self.bot.say(msg)

    @epvpis.error
    async def epvpis_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await self.bot.say(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut')

    @commands.command(pass_context=True, aliases=['verify'])
    @commands.cooldown(1, 5, commands.cooldowns.BucketType.server)
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
        #Coding Lounge
        elif ctx.message.server.id == '161637499939192832':
            verifyRole = 'Verified Account'
        #Coding Lounge 2.0
        elif ctx.message.server.id == '357603732634075136':
            verifyRole = 'Verified e*pvp Account'
        else:
            await self.bot.say('**:no_entry:** This command only works on some selected servers!')
            return

        role = discord.utils.get(ctx.message.server.roles, name=verifyRole)

        if len(user) == 0:
            username = ctx.message.author.name
        else:
            if user[0] == 'remove':
                try:
                    await self.bot.remove_roles(ctx.message.author, role)
                    await self.bot.say(f':ok: Role **{role}** removed')
                except:
                    pass
                finally:
                    return
            else:
                username = ' '.join(user)
        tmp = await self.bot.say(f':ok: Trying to verify Discord user **{ctx.message.author}** with Elitepvpers user **{username}**...')
        await self.bot.send_typing(ctx.message.channel)

        if str(ctx.message.author) == await self._getDiscordTag(username, self.bot.userAgentHeaders):
            if role in ctx.message.author.roles:
                await self.bot.edit_message(tmp, f':negative_squared_cross_mark: You already have the role **{role}**!')
            else:
                try:
                    await self.bot.add_roles(ctx.message.author, role)
                    await self.bot.change_nickname(ctx.message.author, username)
                except:
                    pass
                await self.bot.edit_message(tmp, f':white_check_mark: User **{username}** successfully verified! Added to role **{role}**')
        else:
            await self.bot.edit_message(tmp, f':x: Could not verify Discord user **{ctx.message.author}** with Elitepvpers user **{username}**')
            await self.bot.send_message(ctx.message.author, 'I\'m messaging you because I couldn\'t verify you with your corresponding Elitepvpers account' +
                                   '\n\nYou will need to specify your Elitepvpers username with the `:verify` command in case your Discord username is' +
                                   '**not** the same as your Elitepvpers username.' +
                                   'This can be done via `:verify [YOUR ELITEPVPERS USERNAME]`' +
                                   '\n\nAlso don\'t forget to add your Discord username + discriminator in your elitepvpers settings! ' +
                                   '(<https://www.elitepvpers.com/forum/profile.php?do=editprofile>) \nhttps://i.imgur.com/4ckQsjX.png')

    @epvpverify.error
    async def epvpverify_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await self.bot.say(str(error))
        else:
            await self.bot.say('Having currently difficulties to reach elitepvpers. Try it again in some hours.')

    @commands.command(pass_context=True, aliases=['user'])
    @commands.cooldown(2, 1, commands.cooldowns.BucketType.server)
    async def kokoro(self, ctx, *user: str):
        '''Gibt Benutzerdaten über einen Benutzer aus Kokoro-ko.de aus

        Beispiel:
        -----------

        :kokoro

        :user Eddy
        '''
        if len(user) == 0:
            username = ctx.message.author.name
        else:
            username = user[0]

        url = f'{self.discourseURL}/users/{username}.json'
        async with aiohttp.put(url, data = loadconfig.__discourseAPIKey__) as r:
            if r.status == 200:
                json = await r.json()
                if json['user']['primary_group_flair_bg_color'] == None or True:
                    color = 0xff6600 #orange
                else:
                    #color = hex(int(json['user']['primary_group_flair_bg_color'], 16))
                    color = discord.Color(hex(int(json['user']['primary_group_flair_bg_color'], 16)))
                    print(color.value)
                    #currently not working??
                embed = discord.Embed(color=color)
                embed.set_footer(text='kokoro-ko.de - Dein Anime und Gaming forum')
                avatarURL = self.discourseURL + json['user']['avatar_template']
                embed.set_thumbnail(url=avatarURL.format(size = '124'))
                if json['user']['name'] == '':
                    discordName = json['user']['username']
                else:
                    discordName = '{} ({})'.format(json['user']['username'], json['user']['name'])
                embed.add_field(name='Username', value=discordName, inline=True)
                embed.add_field(name='Vertrauensstufe', value=json['user']['trust_level'], inline=True)
                if json['user']['title'] != '' and json['user']['title'] != None:
                    embed.add_field(name='Titel', value=json['user']['title'], inline=True)
                embed.add_field(name='Registriert am', value=json['user']['created_at'], inline=True)
                embed.add_field(name='Abzeichen', value=json['user']['badge_count'], inline=True)
                embed.add_field(name='Beiträge', value=json['user']['post_count'], inline=True)
                if json['user']['user_fields']['7'] != '' and json['user']['user_fields']['7'] != None:
                    embed.add_field(name='Discord', value=json['user']['user_fields']['7'], inline=True)
                if json['user']['user_fields']['1'] != '' and json['user']['user_fields']['1'] != None:
                    embed.add_field(name='Steam', value='http://steamcommunity.com/id/' + json['user']['user_fields']['1'], inline=True)
                groups = ''
                for group in json['user']['groups']:
                    if group['automatic'] == False:
                        groups += group['name'] + ', '
                if groups != '':
                    embed.add_field(name='Gruppen', value=groups[:-2], inline=True)
                embed.add_field(name='Profile Link', value=f'{self.discourseURL}/users/{username}/summary', inline=True)
                await self.bot.say(embed=embed)
            else:
                msg = f':no_entry: Ich konnte keinen Account **{username}** auf kokoro-ko.de finden :sweat:'
                await self.bot.say(msg)

    @kokoro.error
    async def kokoro_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await self.bot.say(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut')

def setup(bot):
    bot.add_cog(forum(bot))
