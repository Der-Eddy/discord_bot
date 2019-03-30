import os
import asyncio
import aiohttp
import discord
from discord.ext import commands

class gwent(commands.Cog):
    '''Gwent: The Witcher 3 Card Game spezifische Commands'''

    def __init__(self, bot):
        self.bot = bot
        self.APIURL = 'https://api.gwentapi.com/v0/cards?name='

    @commands.command(pass_context=True, aliases=['gwint', 'gwentcard'])
    @commands.cooldown(1, 2, commands.cooldowns.BucketType.server)
    async def gwent(self, ctx, *card: str):
        '''Gibt Informationen zu einer Gwent Karte aus

        Beispiel:
        -----------

        :gwent Geralt
        '''
        cardName = ' '.join(card)
        url = f'{self.APIURL}{cardName}'
        await self.bot.send_typing(ctx.message.channel)
        async with aiohttp.get(url) as firstResult:
            if firstResult.status == 200:
                json = await firstResult.json()
                async with aiohttp.get(json['results'][0]['href']) as r:
                    json = await r.json()
                    async with aiohttp.get(json['variations'][0]['href']) as image:
                        imagejson = await r.json()
                        image = imagejson['art']['thumbnailImage']
                        tempGwentCard = 'tmp\\tempGwent.png'
                        async with aiohttp.get(image) as img:
                            with open(tempGwentCard, 'wb') as f:
                                f.write(await img.read())
                        with open(tempGwentCard, 'rb') as f:
                            await self.bot.send_file(ctx.message.channel, f)
                        os.remove(tempGwentCard)

                    rarity = json['variations'][0]['rarity']['href']
                    if rarity == 'https://api.gwentapi.com/v0/rarities/u0zNKy4EULa_VU4JD5r4EA':
                        color = 0xf1c40f #Legendary
                    elif rarity == 'https://api.gwentapi.com/v0/rarities/-naHV1zlVuCFll-j-7T1ow':
                        color = 0x5D92B1 #Rare
                    elif rarity == 'https://api.gwentapi.com/v0/rarities/V_ImiYfTVhG_WaAOof9Rxg':
                        color = 0x7D61BB #Epic
                    else:
                        color = 0xc0c0c0 #Common
                    embed = discord.Embed(color=color)
                    embed.set_footer(text='UUID: ' + json['uuid'])
                    embed.set_thumbnail(url='https://i.imgur.com/WNYBsYp.png')
                    embed.add_field(name='Name', value=json['name'], inline=True)
                    if json['strength'] != '' and json['strength'] != None:
                        embed.add_field(name='Stärke', value=json['strength'], inline=True)
                    if json['group'] != '' and json['group'] != None:
                        embed.add_field(name='Typ', value=json['group'], inline=True)
                    if rarity != '' and rarity != None:
                        embed.add_field(name='Seltenheit', value=rarity, inline=True)
                    if json['faction'] != '' and json['faction'] != None:
                        embed.add_field(name='Fraktion', value=json['faction']['name'], inline=True)
                    if json['positions'] != '' and json['positions'] != None:
                        embed.add_field(name='Reihe', value=', '.join(json['positions']), inline=True)
                    embed.add_field(name='Text', value=json['info'], inline=False)
                    await self.bot.say(embed=embed)
            else:
                msg = f':no_entry: Ich konnte keine Gwent Karte zu **{cardName}** finden :sweat:'
                await self.bot.say(msg)

    @gwent.error
    async def gwent_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await self.bot.say(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut')

def setup(bot):
    bot.add_cog(gwent(bot))
