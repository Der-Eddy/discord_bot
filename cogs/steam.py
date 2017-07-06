import re
import asyncio
import aiohttp
import discord
from discord.ext import commands

class steam():
    '''Steam spezifische Commands'''

    def __init__(self, bot):
        self.bot = bot
        self.steamSpyAPIURL = 'https://steamspy.com/api.php'
        self.steamCurrentPlayerAPIURL = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v0001/?appid='
        self.steamMarketAPIURL = 'http://store.steampowered.com/api/appdetails/?appids='

    @commands.command(pass_context=True)
    @commands.cooldown(1, 2, commands.cooldowns.BucketType.server)
    async def steam(self, ctx, appid: str):
        '''Gibt Informationen zu einem Spiel bei Steam aus

        Beispiel:
        -----------

        :steam 570
        '''
        await self.bot.send_typing(ctx.message.channel)
        steamSpyURL = f'{self.steamSpyAPIURL}?request=appdetails&appid={appid}'
        async with aiohttp.get(steamSpyURL) as r:
            spyJSON = await r.json()

        steamCurrentPlayerURL = f'{self.steamCurrentPlayerAPIURL}{appid}'
        async with aiohttp.get(steamCurrentPlayerURL) as r:
            currentPlayerJSON = await r.json()

        steamMarketURL = f'{self.steamMarketAPIURL}{appid}'
        async with aiohttp.get(steamMarketURL) as r:
            marketJSON = await r.json()

        owner = '{:,}'.format(spyJSON['owners']).replace(',', '.')
        owner += ' ± '
        owner += '{:,}'.format(spyJSON['owners_variance']).replace(',', '.')

        try:
            price = str(int(marketJSON[appid]['data']['price_overview']['final']) / 100) + '€'
            if marketJSON[appid]['data']['price_overview']['discount_percent'] != 0:
                price += ' (-{}%)'.format(marketJSON[appid]['data']['price_overview']['discount_percent'])
        except KeyError:
            price = 'Free'

        embed = discord.Embed(color=0x2F668D, title=spyJSON['name'], url=f'http://store.steampowered.com/app/{appid}')
        embed.set_footer(text='AppID: {}'.format(spyJSON['appid']))
        embed.set_thumbnail(url=f'http://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg')
        embed.add_field(name='Name', value=spyJSON['name'], inline=True)
        embed.add_field(name='Score Rank', value=spyJSON['score_rank'], inline=True)
        embed.add_field(name='Preis', value=price, inline=True)
        embed.add_field(name='Besitzer', value=owner, inline=True)
        embed.add_field(name='Derzeitige Spieler', value=currentPlayerJSON['response']['player_count'], inline=True)
        embed.add_field(name='Durchschnittliche Spieler gestern', value=spyJSON['ccu'], inline=True)
        embed.add_field(name='Entwickler', value=spyJSON['developer'], inline=True)
        embed.add_field(name='Publisher', value=spyJSON['publisher'], inline=True)
        if marketJSON[appid]['data']['short_description'] != '' and marketJSON[appid]['data']['short_description'] != None:
            discription = re.sub(re.compile('<.*?>'), '', marketJSON[appid]['data']['short_description'])
            embed.add_field(name='Beschreibung', value=discription, inline=False)
        embed.add_field(name='Link', value=f'http://store.steampowered.com/app/{appid}', inline=False)

        await self.bot.say(embed=embed)


    @steam.error
    async def steam_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await self.bot.say(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut')
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await self.bot.say(':x: Konnte keine Verbindung zum Steam API aufbauen')

def setup(bot):
    bot.add_cog(steam(bot))
