import time
import os
import platform
import re
import asyncio
import inspect
from datetime import datetime, timedelta
import aiohttp
import discord
from discord.ext import commands
from memory_profiler import memory_usage
import loadconfig
import checks

#Stolen from https://github.com/Rapptz/RoboDanny/blob/b513a32dfbd4fdbd910f7f56d88d1d012ab44826/cogs/meta.py
class TimeParser:
    def __init__(self, argument):
        compiled = re.compile(r"(?:(?P<hours>[0-9]{1,5})h)?(?:(?P<minutes>[0-9]{1,5})m)?(?:(?P<seconds>[0-9]{1,5})s)?$")
        self.original = argument
        try:
            self.seconds = int(argument)
        except ValueError as e:
            match = compiled.match(argument)
            if match is None or not match.group(0):
                raise commands.BadArgument('Falsche Zeit angegeben, gültig sind z.B. `4h`, `3m` oder `2s`') from e

            self.seconds = 0
            hours = match.group('hours')
            if hours is not None:
                self.seconds += int(hours) * 3600
            minutes = match.group('minutes')
            if minutes is not None:
                self.seconds += int(minutes) * 60
            seconds = match.group('seconds')
            if seconds is not None:
                self.seconds += int(seconds)

        if self.seconds <= 0:
            raise commands.BadArgument('Zu wenig Zeit angegeben, gültig sind z.B. `4h`, `3m` oder `2s`')

        if self.seconds > 604800: # 7 days
            raise commands.BadArgument('7 Tage sind ne lange Zeit, denkste du nicht auch?')

    @staticmethod
    def human_timedelta(dt):
        now = datetime.utcnow()
        delta = now - dt
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)

        if days:
            if hours:
                return '%s und %s' % (Plural(Tag=days), Plural(Stunde=hours))
            return Plural(day=days)

        if hours:
            if minutes:
                return '%s und %s' % (Plural(Stunde=hours), Plural(Minute=minutes))
            return Plural(hour=hours)

        if minutes:
            if seconds:
                return '%s und %s' % (Plural(Minute=minutes), Plural(Sekunde=seconds))
            return Plural(Minute=minutes)
        return Plural(Sekunde=seconds)

class Plural:
    def __init__(self, **attr):
        iterator = attr.items()
        self.name, self.value = next(iter(iterator))

    def __str__(self):
        v = self.value
        if v > 1:
            return '%s %sn' % (v, self.name)
        return '%s %s' % (v, self.name)

class utility():
    '''Allgemeine/nützliche Befehle welche nirgendwo sonst reinpassen'''

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles:
            if not role.is_everyone:
                string += f'{role.mention}, '
        if string is '':
            return 'None'
        else:
            return string[:-2]

    @staticmethod
    def _getEmojis(emojis):
        string = ''
        for emoji in emojis:
            string += str(emoji)
        if string is '':
            return 'None'
        else:
            return string[:1000] #The maximum allowed charcter amount for embed fields

    @commands.command(pass_context=True, aliases=['s', 'uptime', 'up'])
    async def status(self, ctx):
        '''Infos über den Bot'''
        timeUp = time.time() - self.bot.startTime
        hours = timeUp / 3600
        minutes = (timeUp / 60) % 60
        seconds = timeUp % 60

        admin = ''
        users = 0
        channel = 0
        try:
            commandsChart = sorted(self.bot.commands_used.items(), key=lambda t: t[1], reverse=False)
            topCommand = commandsChart.pop()
            commandsInfo = '{} (Top-Command: {} x {})'.format(sum(self.bot.commands_used.values()), topCommand[1], topCommand[0])
        except IndexError:
            commandsInfo = str(sum(self.bot.commands_used.values()))
        botMember = ctx.message.server.get_member(self.bot.user.id)
        for s in self.bot.servers:
            users += len(s.members)
            channel += len(s.channels)
            if not admin: admin = s.get_member(loadconfig.__adminid__)

        embed = discord.Embed(color=botMember.top_role.colour)
        embed.set_footer(text='Dieser Bot ist Open-Source auf GitHub: https://github.com/Der-Eddy/discord_bot')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Admin', value=admin, inline=False)
        embed.add_field(name='Uptime', value='{0:.0f} Stunden, {1:.0f} Minuten und {2:.0f} Sekunden\n'.format(hours, minutes, seconds), inline=False)
        embed.add_field(name='Beobachtete Benutzer', value=users, inline=True)
        embed.add_field(name='Beobachtete Server', value=len(self.bot.servers), inline=True)
        embed.add_field(name='Beobachtete Channel', value=channel, inline=True)
        embed.add_field(name='Ausgeführte Commands', value=commandsInfo, inline=True)
        embed.add_field(name='Bot Version', value=self.bot.botVersion, inline=True)
        embed.add_field(name='Discord.py Version', value=discord.__version__, inline=True)
        embed.add_field(name='Python Version', value=platform.python_version(), inline=True)
        embed.add_field(name='Speicher Auslastung', value='{} MB'.format(round(memory_usage(-1)[0], 3)), inline=True)
        embed.add_field(name='Betriebssystem', value='{} {} {}'.format(platform.system(), platform.release(), platform.version()), inline=False)
        await self.bot.say('**:information_source:** Informationen über diesen Bot:', embed=embed)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        '''Misst die Response Time'''
        ping = ctx.message
        pong = await self.bot.say('**:ping_pong:** Pong!')
        delta = pong.timestamp - ping.timestamp
        delta = int(delta.total_seconds() * 1000)
        await self.bot.edit_message(pong, '**:ping_pong:** Pong! (%d ms)' % delta)

    @commands.command()
    async def github(self):
        '''In progress'''
        await self.bot.say('https://github.com/Der-Eddy/discord_bot')

    @commands.command(pass_context=True, aliases=['info'])
    async def about(self, ctx):
        '''Info über mich'''
        msg = '**:information_source: Shinobu Oshino (500 Jahre alt)**\n'
        msg += '```Shinobu Oshino gehört wohl zu den mysteriösesten Charakteren in Bakemonogatari. Sie war bis vorletzten Frühling ein hochangesehener, adeliger, skrupelloser Vampir, der weit über 500 Jahre alt ist. Gnadenlos griff sie Menschen an und massakrierte sie nach Belieben. Auch Koyomi Araragi wurde von ihr attackiert und schwer verwundet. Nur durch das Eingreifen des Exorzisten Meme Oshino konnte Kiss-shot Acerola-orion Heart-under-blade, wie sie damals bekannt war, bezwungen werden. Dabei verlor sie jedoch all ihre Erinnerungen und wurde von einer attraktiven, erwachsenen Frau in einen unschuldigen Mädchenkörper verwandelt.\n\n'
        msg += 'Seitdem lebt sie zusammen mit Meme in einem verlassenen Gebäude und wurde von ihm aufgenommen. Er gab ihr auch ihren Namen Shinobu. Wann immer man Shinobu sehen sollte, sitzt sie nur mit traurigem Gesicht in einer Ecke und träumt vor sich hin. Sie spricht nicht und wirkt auch sonst meistens sehr abwesend. Einzig und allein zu Koyomi scheint sie ein freundschaftliches Verhältnis zu haben. Das Vampirblut in ihr verlangt immer noch nach Opfern und da sich Koyomi in gewisser Art und Weise schuldig fühlt, stellt er sich regelmäßig als Nahrungsquelle für Shinobu zur Verfügung.\n\n'
        msg += 'Quelle: http://www.anisearch.de/character/6598,shinobu-oshino/```\n\n'
        msg += 'Dieser Bot ist außerdem **:free:**, Open-Source, in Python und mit Hilfe von discord.py geschrieben! <https://github.com/Der-Eddy/discord_bot>\n'
        with open('img/ava.png', 'rb') as f:
            await self.bot.send_file(ctx.message.channel, f, content=msg)

    @commands.command(pass_context=True, aliases=['archive'])
    async def log(self, ctx, *limit: int):
        '''Archiviert den Log des derzeitigen Channels und läd diesen als Attachment hoch

        Beispiel:
        -----------

        :log 100
        '''
        try:
            limit = int(limit[0])
        except IndexError:
            limit = 10
        logFile = '{}.log'.format(ctx.message.channel)
        counter = 0
        with open(logFile, 'w', encoding='UTF-8') as f:
            f.write('Archivierte Nachrichten vom Channel: {} am {}\n'.format(ctx.message.channel, ctx.message.timestamp.strftime('%d.%m.%Y %H:%M:%S')))
            async for message in self.bot.logs_from(ctx.message.channel, limit=limit, before=ctx.message):
                try:
                    attachment = '[Angehängte Datei: {}]'.format(message.attachments[0]['url'])
                except IndexError:
                    attachment = ''
                f.write('{} {!s:20s}: {} {}\n'.format(message.timestamp.strftime('%d.%m.%Y %H:%M:%S'), message.author, message.clean_content, attachment))
                counter += 1
        msg = ':ok: {} Nachrichten wurden archiviert!'.format(counter)
        with open(logFile, 'rb') as f:
            await self.bot.send_file(ctx.message.channel, f, content=msg)
        os.remove(logFile)

    @commands.command()
    async def invite(self):
        '''Verschickt einen Invite für den Server des Bot Autors'''
        permInvite = 'https://discord.gg/kPMbPDc'
        msg = '**:cool:** ' + permInvite
        await self.bot.say(msg)

    @commands.command()
    async def whois(self, member: discord.Member=None):
        '''Gibt Informationen über einen Benutzer aus

        Beispiel:
        -----------

        :whois @Der-Eddy#6508
        '''

        if member.top_role.is_everyone:
            topRole = 'everyone' #to prevent @everyone spam
            topRoleColour = '#000000'
        else:
            topRole = member.top_role
            topRoleColour = member.top_role.colour

        if member is not None:
            embed = discord.Embed(color=member.top_role.colour)
            embed.set_footer(text='UserID: {}'.format(member.id))
            embed.set_thumbnail(url=member.avatar_url)
            if member.name != member.display_name:
                fullName = '{} ({})'.format(member, member.display_name)
            else:
                fullName = member
            embed.add_field(name=member.name, value=fullName, inline=False)
            embed.add_field(name='Discord beigetreten am', value='{}\n(Tage seitdem: {})'.format(member.created_at.strftime('%d.%m.%Y'), (datetime.now()-member.created_at).days), inline=True)
            embed.add_field(name='Server beigetreten am', value='{}\n(Tage seitdem: {})'.format(member.joined_at.strftime('%d.%m.%Y'), (datetime.now()-member.joined_at).days), inline=True)
            embed.add_field(name='Avatar Link', value=member.avatar_url, inline=False)
            embed.add_field(name='Rollen', value=self._getRoles(member.roles), inline=True)
            embed.add_field(name='Rollenfarbe', value='{} ({})'.format(topRoleColour, topRole), inline=True)
            await self.bot.say('', embed=embed)
        else:
            msg = '**:no_entry:** Du hast keinen Benutzer angegeben!'
            await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['e'])
    async def emoji(self, ctx, emojiname: str):
        '''Gibt eine vergrößerte Version eines angegebenen Emojis zurück

        Beispiel:
        -----------

        :emoji Emilia
        '''
        emoji = discord.utils.find(lambda e: e.name.lower() == emojiname.lower(), self.bot.get_all_emojis())
        if emoji:
            tempEmojiFile = 'tempEmoji.png'
            async with aiohttp.get(emoji.url) as img:
                with open(tempEmojiFile, 'wb') as f:
                    f.write(await img.read())
            with open(tempEmojiFile, 'rb') as f:
                await self.bot.send_file(ctx.message.channel, f)
            os.remove(tempEmojiFile)
        else:
            await self.bot.say(':x: Konnte das angegebene Emoji leider nicht finden :(')

    @commands.command(aliases=['emotes'])
    async def emojis(self):
        '''Gibt alle Emojis aus auf welche der Bot Zugriff hat'''
        msg = ''
        for emoji in self.bot.get_all_emojis():
            if len(msg) + len(str(emoji)) > 1000:
                await self.bot.say(msg)
                msg = ''
            msg += str(emoji)
        await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['serverinfo', 'guild', 'membercount'])
    async def server(self, ctx):
        '''Gibt Informationen über die derzeitge Discord Guild aus'''
        emojis = self._getEmojis(ctx.message.server.emojis)
        print(emojis)
        roles = self._getRoles(ctx.message.server.role_hierarchy)
        embed = discord.Embed(color=0xf1c40f) #Golden
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.set_footer(text='Es können evtl. Emojis fehlen')
        embed.add_field(name='Name', value=ctx.message.server.name, inline=True)
        embed.add_field(name='ID', value=ctx.message.server.id, inline=True)
        embed.add_field(name='Besitzer', value=ctx.message.server.owner, inline=True)
        embed.add_field(name='Region', value=ctx.message.server.region, inline=True)
        embed.add_field(name='Mitglieder', value=ctx.message.server.member_count, inline=True)
        embed.add_field(name='Erstellt am', value=ctx.message.server.created_at.strftime('%d.%m.%Y'), inline=True)
        embed.add_field(name='Standard Channel', value=f'#{ctx.message.server.default_channel}', inline=True)
        embed.add_field(name='AFK Voice Timeout', value=f'{int(ctx.message.server.afk_timeout / 60)} min', inline=True)
        embed.add_field(name='Rollen', value=roles, inline=True)
        embed.add_field(name='Custom Emojis', value=emojis, inline=True)
        await self.bot.say(embed=embed)

    #Shameful copied from https://github.com/Rapptz/RoboDanny/blob/b513a32dfbd4fdbd910f7f56d88d1d012ab44826/cogs/meta.py
    @commands.command(pass_context=True, aliases=['reminder'])
    async def timer(self, ctx, time : TimeParser, *, message=''):
        '''Setzt einen Timer und benachrichtigt dann einen

        Beispiel:
        -----------

        :timer 13m Pizza

        :timer 2h Stream startet
        '''
        author = ctx.message.author
        reminder = None
        completed = None
        message = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')

        if not message:
            reminder = ':timer: Ok {0.mention}, Ich stelle einen Timer auf {1}.'
            completed = ':alarm_clock: Ding Ding Ding {0.mention}! Dein Timer ist abgelaufen.'
        else:
            reminder = ':timer: Ok {0.mention}, Ich stelle einen Timer für `{2}` auf {1}.'
            completed = ':alarm_clock: Ding Ding Ding {0.mention}! Dein Timer für `{1}` ist abgelaufen.'

        human_time = datetime.utcnow() - timedelta(seconds=time.seconds)
        human_time = TimeParser.human_timedelta(human_time)
        await self.bot.say(reminder.format(author, human_time, message))
        await asyncio.sleep(time.seconds)
        await self.bot.say(completed.format(author, message, human_time))

    @timer.error
    async def timer_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            await self.bot.say(str(error))

    #Stolen from https://github.com/Rapptz/RoboDanny/blob/b513a32dfbd4fdbd910f7f56d88d1d012ab44826/cogs/meta.py
    @commands.command()
    async def source(self, *, command: str = None):
        '''Zeigt den Quellcode für einen Befehl auf GitHub an

        Beispiel:
        -----------

        :source kawaii
        '''
        source_url = 'https://github.com/Der-Eddy/discord_bot'
        if command is None:
            await self.bot.say(source_url)
            return

        obj = self.bot.get_command(command.replace('.', ' '))
        if obj is None:
            return await self.bot.say(':x: Konnte den Befehl nicht finden')

        # since we found the command we're looking for, presumably anyway, let's
        # try to access the code itself
        src = obj.callback.__code__
        lines, firstlineno = inspect.getsourcelines(src)
        sourcecode = inspect.getsource(src).replace('```', '')
        if not obj.callback.__module__.startswith('discord'):
            # not a built-in command
            location = os.path.relpath(src.co_filename).replace('\\', '/')
        else:
            location = obj.callback.__module__.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'

        if len(sourcecode) > 1900:
            final_url = '{}/blob/master/{}#L{}-L{}'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1)
        else:
            final_url = '<{}/blob/master/{}#L{}-L{}>\n```Python\n{}```'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1, sourcecode)

        await self.bot.say(final_url)

    # This command needs to be at the end due to this name
    @commands.command()
    async def commands(self):
        '''Zeigt an wie oft welcher Command benutzt wurde seit dem letzten Startup'''
        msg = ':chart: Liste der ausgeführten Befehle (seit letztem Startup)\n'
        msg += 'Insgesamt: {}\n'.format(sum(self.bot.commands_used.values()))
        msg += '```js\n'
        msg += '{!s:15s}: {!s:>4s}\n'.format('Name', 'Anzahl')
        chart = sorted(self.bot.commands_used.items(), key=lambda t: t[1], reverse=True)
        for name, amount in chart:
            msg += '{!s:15s}: {!s:>4s}\n'.format(name, amount)
        msg += '```'
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(utility(bot))
