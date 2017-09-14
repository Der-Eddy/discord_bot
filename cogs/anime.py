import sys
import random
import re
import asyncio
import aiohttp
import discord
from discord.ext import commands
import loadconfig

class anime():
    '''Alles rund um Animes'''
    kawaiich = loadconfig.__kawaiichannel__
    nsfwRole = loadconfig.__selfassignrole__

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

    @commands.command(pass_context=True, hidden=True)
    async def nsfw(self, ctx):
        '''Vergibt die Rolle um auf die NSFW Channel zugreifen zu können'''
        if ctx.message.server == self.bot.get_server(loadconfig.__botserverid__):
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
            tmp = await self.bot.say('**:no_entry:** This command will only works on the server of <@{}>!'.format(__adminid__))
        await asyncio.sleep(2 * 60)
        await self.bot.delete_message(tmp)
        await self.bot.delete_message(ctx.message)

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
        nepnep = ['topnep',
                  'Can\'t pep the nep',
                  'Flat is justice',
                  'nep nep nep nep nep nep nep nep nep nep nep',
                  'Nepgear > your waifu']
        msg = '{} {}'.format(random.choice(nepnep), random.choice(neps))
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def pat(self, ctx, member: discord.Member = None):
        '''/r/headpats Pat Pat Pat :3

        Beispiel:
        -----------

        :pat @Der-Eddy#6508
        '''
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
                    'https://i.imgur.com/IqGRUu4.gif',
                    'https://68.media.tumblr.com/f95f14437809dfec8057b2bd525e6b4a/tumblr_omvkl2SzeK1ql0375o1_500.gif']
            msg = '{} tätschelt dich {} :3 \n{}'.format(ctx.message.author.mention, member.mention, random.choice(gifs))
            await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['rate', 'waifu'])
    async def ratewaifu(self, ctx, *, waifuName: str):
        '''Rate my waifu

        Beispiel:
        -----------

        :ratewaifu Sagiri
        '''
        waifu = waifuName.lower()
        bestWaifus = ['kobeni', 'emilia', 'shinobu', 'karen', 'shouko', 'minori',
                      'chidori', 'sagiri', 'mashiro', 'last order', 'saki', 'makoto',
                      'yui', 'nep', 'neptunia', 'taiga']
        trashWaifus = ['shino', 'rikka']
        if waifu in bestWaifus:
            rating = 10
        elif waifu in trashWaifus:
            rating = 0
        else:
            rating = hash(waifu) % 10

        if waifu == 'emilia':
            emoji = '<:Emilia:230684388084416512>'
        elif waifu == 'shinobu':
            emoji = '<:Shinobu:303302053688770561>'
        elif waifu == 'mashiro':
            emoji = '<:mashiro:266233568626343936>'
        elif waifu == 'nep' or waifu == 'neptunia':
            emoji = '<:nep:261230988758220822>'
        elif rating < 2:
            emoji = ':put_litter_in_its_place:'
        elif rating < 5:
            emoji = '<:k3llyLUL:341946977266827264>'
        elif rating < 7:
            emoji = '<:k3llyTHINK:341946932639432704>'
        elif rating < 9:
            emojis = ['<:faeGasm:298772756412104704>', '<:naroGasm:341200647741243393>']
            emoji = random.choice(emojis)
        elif rating < 10:
            emojis = ['<:kanoLewd:230662559458525185>', '<:fowShy:230662561580843008>', '<:mendoLewd:230662561169801216>']
            emoji = random.choice(emojis)
        elif rating == 10:
            emojis = ['<:okhand:335170448666918923>', '<:nepnep:314906910061101057>', '<:gaku:249970768786489345>', '<:faeWant:313430419661914113>']
            emoji = random.choice(emojis)

        msg = f'{emoji} Ich bewerte **{waifuName}** als **{rating}/10**'
        await self.bot.say(msg)

    @commands.command(pass_context=True, hidden=True)
    async def imgur(self, ctx, amount: int = None):
        '''Lädt eine bestimmte Anzahl der letzten hochgeladenen Bilder im Channel bei Imgur hoch'''
        await self.bot.say(':new: Befehl in Arbeit!')

    @commands.command(pass_context=True, alias=['ani'], hidden=True)
    async def anisearch(self, ctx, url: str = None):
        '''Gibt Informationen über einen AniSearch.de User zurück'''
        async with aiohttp.get(url) as r:
            if r.status == 200:
                content = await r.text()
                animeRE = r"<td class=\"rtype2\">\w+</td><td>(\d+)</td>"
                watchedAnimes = re.search(content, animeRE)
                await self.bot.say(str(watchedAnimes.group(0)))
            else:
                await self.bot.say(':x: Konnte den Benutzer nicht finden (falsche URL?)')

def setup(bot):
    bot.add_cog(anime(bot))
