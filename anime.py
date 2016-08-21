import discord
from discord.ext import commands
import sys
import asyncio
import aiohttp
import random
import sqlite3

try:
    from config import __token__, __prefix__, __adminid__, __adminrole__, __modrole__, __kawaiichannel__, __botlogchannel__, __github__, __botserverid__, __greetmsg__, __selfassignrole__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __botserverid__ = os.environ.get('DISCORD_BOTSERVERID')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __adminrole__ = os.environ.get('DISCORD_ADMINROLE')
    __modrole__ = os.environ.get('DISCORD_MODROLE')
    __kawaiichannel__ = os.environ.get('DISCORD_KAWAIICHANNEL')
    __botlogchannel__ = os.environ.get('DISCORD_BOTLOGCHANNEL')
    __github__ = os.environ.get('DISCORD_GITHUB')
    __greetmsg__ = os.environ.get('DISCORD_GREETMSG')
    __selfassignrole__ = os.environ.get('DISCORD_SELFASSIGNROLE')

class anime():
    '''Alles rund um Animes'''
    kawaiich = __kawaiichannel__
    nsfwRole = __selfassignrole__
    mod = __modrole__
    db = 'reaction.db'

    def __init__(self, bot):
        self.bot = bot

    def checkRole(self, user, roleRec):
        ok = False
        for all in list(user.roles):
            if all.name == roleRec:
                ok = True
        return ok

    @commands.command(pass_context=True)
    async def kawaii(self, ctx):
        '''Gibt ein zufälliges kawaii Bild aus'''
        if self.kawaiich:
            pins = await self.bot.pins_from(self.bot.get_channel(self.kawaiich))
            rnd = random.choice(pins)
            try:
                img = rnd.attachments[0]['url']
            except IndexError:
                img = rnd.content
            emojis = [':blush:', ':flushed:', ':heart_eyes:', ':heart_eyes_cat:', ':heart:']
            await self.bot.say('{2} Von: {0}: {1}'.format(rnd.author.display_name, img, random.choice(emojis)))
        else:
            await self.bot.say('**:no_entry:** Es wurde kein Channel für den Bot eingestellt! Wende dich bitte an den Bot Admin')

    @commands.command(pass_context=True)
    async def nsfw(self, ctx):
        '''Vergibt die Rolle um auf die NSFW Channel zugreifen zu können'''
        if self.nsfwRole:
            member = ctx.message.author
            role = discord.utils.get(ctx.message.server.roles, name=self.nsfwRole)
            if role in member.roles:
                try:
                    await self.bot.remove_roles(member, role)
                except:
                    pass
                tmp = await self.bot.say(':x: Rolle **{0}** wurde entfernt'.format(role))
            else:
                try:
                    await self.bot.add_roles(member, role)
                except:
                    pass
                tmp = await self.bot.say(':white_check_mark: Rolle **{0}** wurde hinzugefügt'.format(role))
        else:
            tmp = await self.bot.say('**:no_entry:** Es wurde keine Rolle für den Bot eingestellt! Wende dich bitte an den Bot Admin')
        await asyncio.sleep(10)
        await self.bot.delete_message(tmp)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def reaction(self, ctx, command: str, *arg):
        '''Fügt reaction Bilder hinzu oder gibt diese aus'''
        with sqlite3.connect(self.db) as con:
            c = con.cursor()
            if command == 'add':
                if len(arg) > 1:
                    c.execute('INSERT INTO "reactions" ("command","url","author") VALUES (?, ?, ?)', (arg[0].lower(), arg[1], str(ctx.message.author)))
                    con.commit()
                    await self.bot.say(':ok: Command **{}** hinzugefügt!'.format(arg[0].lower()))
            elif command == 'del':
                if self.checkRole(ctx.message.author, self.mod):
                    c.execute('DELETE FROM "reactions" WHERE "id" in (?)', (int(arg[0]), ))
                else:
                    c.execute('DELETE FROM "reactions" WHERE "id" in (?) AND "author" IN (?)', (int(arg[0]), str(ctx.message.author)))
                con.commit()
                await self.bot.say(':put_litter_in_its_place: ID #{} gelöscht!'.format(arg[0].lower()))
            elif command == 'list':
                lst = c.execute('SELECT * FROM "reactions"')
                msg = ''
                for i in lst:
                    msg += '**ID:** {:>3} | **Command:** {:>10} | **URL:** `{}` | **Author:** {}\n'.format(i[0], i[1], i[2], i[3])
                await self.bot.say(msg)
            else:
                lst = c.execute('SELECT * FROM "reactions" WHERE "command" LIKE (?)', (command,))
                reaction = random.choice(lst.fetchall())
                emojis = [':blush:', ':flushed:', ':heart_eyes:', ':heart_eyes_cat:', ':heart:']
                msg = '{} {} *(Von {} | ID: {})*'.format(random.choice(emojis), reaction[2], reaction[3], reaction[0])
                await self.bot.say(msg)
            c.close()

    @commands.command(pass_context=True)
    async def imgur(self, ctx, amount: int = None):
        '''Lädt eine bestimmte Anzahl der letzten hochgeladenen Bilder im Channel bei Imgur hoch'''
        pass

def setup(bot):
    bot.add_cog(anime(bot))
