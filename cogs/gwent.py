import os
import asyncio
import aiohttp
import discord
from discord.ext import commands

class gwent():
    '''Gwent: The Witcher 3 Card Game spezifische Commands'''

    def __init__(self, bot):
        self.bot = bot
        self.APIURL = 'https://gwent-api.herokuapp.com/card/name/'

    @commands.command(pass_context=True, aliases=['gwint', 'gwentcard'])
    @commands.cooldown(1, 2, commands.cooldowns.BucketType.server)
    async def gwent(self, ctx, *card: str):
        '''Gibt Informationen zu einer Gwent Karte aus

        Beispiel:
        -----------

        :gwent Operator
        '''
        cardName = ' '.join(card)
        url = f'{self.APIURL}{cardName}'
        await self.bot.send_typing(ctx.message.channel)
        async with aiohttp.get(url) as r:
            if r.status == 200:
                json = await r.json()

                image = json['image']
                tempGwentCard = 'tmp\\tempGwent.png'
                async with aiohttp.get(image) as img:
                    with open(tempGwentCard, 'wb') as f:
                        f.write(await img.read())
                with open(tempGwentCard, 'rb') as f:
                    await self.bot.send_file(ctx.message.channel, f)
                os.remove(tempGwentCard)

                if json['rarity'] == 'legendary':
                    color = 0xf1c40f
                elif json['rarity'] == 'rare':
                    color = 0x5D92B1
                elif json['rarity'] == 'epic':
                    color = 0x7D61BB
                else:
                    color = 0xc0c0c0
                embed = discord.Embed(color=color)
                embed.set_footer(text='https://www.playgwent.com | Das Witcher 3 Card Game')
                embed.set_thumbnail(url='https://i.imgur.com/WNYBsYp.png')
                embed.add_field(name='Name', value=json['name'], inline=True)
                if json['strength'] != '' and json['strength'] != None:
                    embed.add_field(name='Stärke', value=json['strength'], inline=True)
                if json['traits'] != '' and json['traits'] != None:
                    embed.add_field(name='Traits', value=json['traits'], inline=True)
                if json['group'] != '' and json['group'] != None:
                    embed.add_field(name='Typ', value=json['group'], inline=True)
                if json['rarity'] != '' and json['rarity'] != None:
                    embed.add_field(name='Seltenheit', value=json['rarity'], inline=True)
                if json['faction'] != '' and json['faction'] != None:
                    embed.add_field(name='Fraktion', value=json['faction'], inline=True)
                if json['lane'] != '' and json['lane'] != None:
                    embed.add_field(name='Reihe', value=json['lane'], inline=True)
                if json['loyalty'] != '' and json['loyalty'] != None:
                    embed.add_field(name='Loyalität', value=json['loyalty'], inline=True)
                embed.add_field(name='Text', value=json['text'], inline=False)
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
