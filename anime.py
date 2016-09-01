import discord
from discord.ext import commands
import sys
import asyncio
import aiohttp
import random
import sqlite3

try:
    from config import __token__, __prefix__, __adminid__, __kawaiichannel__, __botlogchannel__, __github__, __botserverid__, __greetmsg__, __selfassignrole__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __botserverid__ = os.environ.get('DISCORD_BOTSERVERID')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
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
        if ctx.message.server == self.bot.get_server(__botserverid__):
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
        else:
            tmp = await self.bot.say('**:no_entry:** Dieser Befehl funktioniert nur auf dem Server von <@{}>!'.format(__adminid__))
        await asyncio.sleep(2 * 60)
        await self.bot.delete_message(tmp)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, enabled=False, hidden=True)
    async def reactionold(self, ctx, command: str, *arg):
        '''OBSOLOTE Fügt reaction Bilder hinzu oder gibt diese aus

        Benutzung:
        -----------

        :reaction COMMAND
            Gibt ein zufälliges Bild unter dem command aus

        :reaction add COMMAND BILDURL
            Fügt das jeweilige Bild zum jeweiligen command hinzu

        :reaction del ID
            Löscht den Eintrag mit der jeweiligen ID, nur für Modaratoren und Ersteller des Eintrags

        :reaction list
            Gibt die volle Liste an commands und jeweiligen Links
        '''
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

    @commands.command(aliases=['wave', 'hi', 'ohaiyo'])
    async def hello(self):
        '''Nonsense gifs zum Hallo sagen'''
        gifs = ['https://cdn.discordapp.com/attachments/102817255661772800/219512763607678976/large_1.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219512898563735552/large.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518948251664384/WgQWD.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518717426532352/tumblr_lnttzfSUM41qgcvsy.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519191290478592/tumblr_mf76erIF6s1qj96p1o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519729604231168/giphy_3.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519737971867649/63953d32c650703cded875ac601e765778ce90d0_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519738781368321/17201a4342e901e5f1bc2a03ad487219c0434c22_hq.gif']
        msg = ':wave: {}'.format(random.choice(gifs))
        await self.bot.say(msg)

    @commands.command(aliases=['nepu', 'topnep'])
    async def nep(self):
        '''Can't stop the Nep'''
        neps = ['https://cdn.discordapp.com/attachments/102817255661772800/219530759881359360/community_image_1421846157.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535598187184128/tumblr_nv25gtvX911ubsb68o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535698309545984/tumblr_mpub9tTuZl1rvrw2eo2_r1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535820430770176/dd9f3cc873f3e13fe098429388fc24242a545a21_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535828773371904/tumblr_nl62nrrPar1u0bcbmo1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535828995538944/dUBNqIH.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535906942615553/b3886374588ec93849e1210449c4561fa699ff0d_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536353841381376/tumblr_nl9wb2qMFD1u3qei8o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536345176080384/tumblr_njhahjh1DB1t0co30o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536356223877120/tumblr_njkq53Roep1t0co30o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536424121139210/tumblr_oalathnmFC1uskgfro1_400.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536451807739904/tumblr_nfg22lqmZ31rjwa86o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536686529380362/tumblr_o98bm76djb1vv3oz0o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219537181440475146/tumblr_mya4mdVhDv1rmk3cyo1_500.gif',
                'https://i.imgur.com/4xnJN9x.png',
                'https://i.imgur.com/bunWIWD.jpg']
        msg = 'topnep {}'.format(random.choice(neps))
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def pat(self, ctx, member: discord.Member = None):
        '''/r/headpats Pat Pat Pat :3'''
        if member is not None:
            gifs = ['https://gfycat.com/PoisedWindingCaecilian',
                    'https://cdn.awwni.me/sou1.jpg',
                    'https://i.imgur.com/Nzxa95W.gifv',
                    'https://cdn.awwni.me/sk0x.png',
                    'https://i.imgur.com/N0UIRkk.png',
                    'https://puu.sh/kz9Bi/8db6286d67.gif',
                    'https://cdn.awwni.me/r915.jpg',
                    'https://i.imgur.com/VRViMGf.gifv',
                    'https://i.imgur.com/73dNfOk.gifv',
                    'https://i.imgur.com/UXAKjRc.jpg',
                    'https://i.imgur.com/dzlDuNs.jpg',
                    'https://i.imgur.com/hPR7SOt.gif',
                    'https://i.imgur.com/IqGRUu4.gif']
            msg = '{} tätschelt dich {} :3 \n{}'.format(ctx.message.author.mention, member.mention, random.choice(gifs))
            await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def imgur(self, ctx, amount: int = None):
        '''Lädt eine bestimmte Anzahl der letzten hochgeladenen Bilder im Channel bei Imgur hoch'''
        await self.bot.say(':new: Befehl in Arbeit!')

def setup(bot):
    bot.add_cog(anime(bot))
