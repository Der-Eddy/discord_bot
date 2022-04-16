import random
import urllib.parse
import sqlite3
import asyncio
import aiohttp
import discord
from discord.ext import commands
import loadconfig

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    def userOnline(self, memberList):
        online = []
        for i in memberList:
            if i.status == discord.Status.online and i.bot == False:
                online.append(i)
        return online

    @commands.command(aliases=['javascript', 'nodejs', 'js'])
    async def java(self, ctx):
        '''Weil Java != Javscript'''
        await ctx.send(':interrobang: Meintest du jQuery, Javascript oder Node.js? https://abload.de/img/2016-05-102130191kzpu.png')

    @commands.command(aliases=['c++', 'c#', 'objective-c'])
    async def csharp(self, ctx):
        '''Wie soll man da überhaupt durchblicken???'''
        await ctx.send(':interrobang: Meintest du C, C++, C# oder Objective-C? https://i.imgur.com/Nd4aAXO.png')

    @commands.command()
    async def praise(self, ctx):
        '''Praise the Sun'''
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def css(self, ctx):
        '''Counter Strike: Source'''
        await ctx.send('http://i.imgur.com/TgPKFTz.gif')

    @commands.command()
    async def countdown(self, ctx):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('**:ok:** DING DING DING')

    @commands.command(aliases=['cat', 'randomcat'])
    async def neko(self, ctx):
        '''Zufällige Katzen Bilder nyan~'''
        #http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                res = await r.json()
                emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
                await ctx.send(random.choice(emojis) + res['file'])


    @commands.command(aliases=['rand'])
    async def random(self, ctx, *arg):
        '''Gibt eine zufällige Zahl oder Member aus

        Benutzung:
        -----------

        :random
            Gibt eine zufällige Zahl zwischen 1 und 100 aus

        :random coin
            Wirft eine Münze (Kopf oder Zahl)

        :random 6
            Gibt eine zufällige Zahl zwischen 1 und 6 aus

        :random 10 20
            Gibt eine zufällige Zahl zwischen 10 und 20 aus

        :random user
            Gibt einen zufällige Benutzer der gerade online ist aus
        
        :random choice Dani Eddy Shinobu
            Wählt aus der vorgegebenen Liste einen Namen aus
        '''
        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['Kopf', 'Zahl']
                await ctx.send(f':arrows_counterclockwise: {random.choice(coin)}')
                return
            elif arg[0] == 'choice':
                choices = list(arg)
                choices.pop(0)
                await ctx.send(f':congratulations: The winner is {random.choice(choices)}')
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.guild.members)
                randomuser = random.choice(online)
                if ctx.channel.permissions_for(ctx.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                await ctx.send(f':congratulations: The winner is {user}')
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) == 2:
                start = int(arg[0])
                end = int(arg[1])
            await ctx.send(f'**:arrows_counterclockwise:** Zufällige Zahl ({start} - {end}): {random.randint(start, end)}')

    @commands.command()
    async def steinigt(self, ctx, member:str):
        '''Monty Python'''
        await ctx.send(f'R.I.P. {member}\nhttps://media.giphy.com/media/l41lGAcThnMc29u2Q/giphy.gif')

    @commands.command(aliases=['hypu', 'train'])
    async def hype(self, ctx):
        '''HYPE TRAIN CHOO CHOO'''
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)

    @commands.command()
    async def xkcd(self, ctx,  *searchterm: str):
        '''Zeigt den letzten oder zufälligen XKCD Comic

        Beispiel:
        -----------

        :xkcd

        :xkcd random
        '''
        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl.format('/')) as r:
                js = await r.json()
                if ''.join(searchterm) == 'random':
                    randomComic = random.randint(0, js['num'])
                    async with cs.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], js['alt'], comicUrl, date)
                await ctx.send(msg)

    @commands.command(aliases=['witz', 'joke'])
    async def pun(self, ctx):
        '''Weil jeder schlechte Witze mag'''
        #ToDo: Add some way to fetch https://github.com/derphilipp/Flachwitze
        puns = ['Was sagt das eine Streichholz zum anderen Streichholz?\n Komm, lass uns durchbrennen',
                'Wieviele Deutsche braucht man um eine Glühbirne zu wechseln?\n Einen, wir sind humorlos und effizient.',
                'Wo wohnt die Katze?\n Im Miezhaus.',
                'Wie begrüßen sich zwei plastische Chirurgen?\n "Was machst du denn heute für ein Gesicht?"',
                'Warum essen Veganer kein Huhn?\n Könnte Ei enthalten',
                '85% der Frauen finden ihren Arsch zu dick, 10% zu dünn, 5% finden ihn so ok, wie er ist und sind froh, dass sie ihn geheiratet haben...',
                'Meine Freundin meint, ich wär neugierig...\n...zumindest\' steht das in ihrem Tagebuch.',
                '"Schatz, Ich muss mein T-Shirt waschen! Welches Waschmaschinen Programm soll ich nehmen?" - "Was steht denn auf dem T-Shirt drauf?"\n "Slayer!"',
                'Gestern erzählte ich meinem Freund, dass ich schon immer dieses Ding aus Harry Potter reiten wollte.\n"einen Besen?" "nein, Hermine."',
                'Warum gehen Ameisen nicht in die Kirche?\nSie sind in Sekten.',
                'Was steht auf dem Grabstein eines Mathematikers?\n"Damit hat er nicht gerechnet."',
                'Wenn ein Yogalehrer seine Beine senkrecht nach oben streckt und dabei furzt, welche Yoga Figur stellt er da?\n Eine Duftkerze',
                'Warum ging der Luftballon kaputt?\n Aus Platzgründen.',
                'Ich wollte Spiderman anrufen, aber er hatte kein Netz und beim Bäcker war alles belegt.',
                'Was vermisst eine Schraube am meisten? Einen Vater',
                'Geht ein Panda über die Straße. Bam....Bus!',
                'Unterhalten sich zwei Gletscher. Sagt der eine: "Was meinst du, was wird die Zukunft bringen?" Sagt der Andere: "Naja, wir werden Seen."',
                'Wenn sich ein Professor ein Brot macht ist das dann wissenschaftlich belegt?',
                'Knabbern zwei Männern an einer Eisenbahnschiene. Sagt der eine: "Ganz schön hart, oder?"\nSagt der andere: "Aber guck mal, da drübern ist ne Weiche"',
                'Warum sind bei IKEA Pfeile auf dem Boden?\nWeil es ein Einrichtungshaus ist',
                'Was macht die Security in der Nudelfabrik?\nDie Pasta auf.',
                'Wie nennt man einen kleinwüchsigen Securitymenschen?\nSicherheitshalber',
                'Habe bei Weight Watchers angerufen. Hat keiner abgenommen.\nDanach beim DJ. Hat aber aufgelegt.'
                'Meine Schwester hat eine Tochter bekommen.\nDa wurde mein Wunsch nach einem Neffen zur Nichte gemacht.',
                'Praktizieren sie Inzest?\n"Mitnichten"',
                'Wann sinkt ein U-Boot?\nAm Tag der offenen Tür.',
                'Auf St. Pauli wurde letztens ein Sarg gefunden. Er konnte aber nicht geöffnet werden, war ein Zuhälter drin!',
                'Treffen sich zwei Anwälte. Fragt der eine "Na, wie geht\'s?" Antwortet der andere "Schlecht. Ich kann nicht klagen"',
                'Treffen sich zwei Jäger. Beide tot.',
                'Treffen sich zwei Päpste.',
                'Treffen sich zwei Psychologen, sagt der eine: "Dir geht\'s gut, wie geht\'s mir?"',
                'Treffen sich zwei Linksextreme in einer Bar, kommen drei Splittergruppen raus.',
                'Was macht man mit nem Hund ohne Beine?\nUm die Häuser ziehen.',
                'Wo findest du nen Hund ohne Beine?\nDa wo du ihn liegen lassen hast.',
                'Was macht eine Bombe im Bordell?\nPuff',
                'Und was macht eine Bombe im Treppenhaus?\nHochgehen',
                'Wo war Lucy nach der Explosion?\nÜberall',
                'Egal, wie dicht du bist. Göthe war dichter!',
                'Egal, wie gut du fährst. Züge fahren Güter!',
                'Egal, wie sauer du bist, Dinos sind Saurier!',
                'Egal, wie leer du bist, es gibt Menschen die sind Lehrer.',
                'Wissenschaftler haben herausgefunden\nund sind dann wieder reingegangen.',
                'Was ist klein, braun, rund und sitzt hinter Gittern? Eine Knastanie.',
                'Was liegt am Strand und kann nicht richtig reden? - Eine Nuschel!',
                'Was ist grün und klopft an die Tür? - Klopfsalat',
                'Was ist rot und steht am Straßenrand? Eine Hagenutte',
                'Und was ist blau und steht am Wegesrand? Eine Frostituierte',
                'Was ist rosa und schwimmt durchs Meer? Eine Meerjungsau.',
                'Was ist braun und schwimmt auch im Meer? Ein U-Brot.',
                'Was raucht und springt durch den Wald? Ein Kaminchen.',
                'Was machen Bits am liebsten? Busfahren.',
                'Warum ist der Programmierer in der Dusche gestorben? Auf der Flasche stand “einschäumen, ausspülen, wiederholen"',
                'Wo gehen Datenspeicher hin, wenn sie sich prügeln wollen? In den Byte Club.\n Und Regel Nummer Eins: Ihr verliert kein dword über den Byte Club!',
                'Wer wohnt im Dschungel und schummelt? Mogli',
                'Geht ein Mann zum Arzt weil er sich schlecht fühlt. Sagt der Arzt: "Sie müssen mit dem Masturbieren aufhören!"\nSagt der Mann: "Wieso das denn?!".\nSagt der Arzt: "Ja, sonst kann ich Sie nicht untersuchen."',
                'Wie heißt ein Spanier ohne Auto?\nCarlos',
                'Wie nennt man ein Cowboy ohne Pferd?\nSattelschlepper',
                'Kommt ein Cowboy aus dem Frisiersalon heraus\nPony weg',
                'Wie nennt man einen Schäfer, der seine Schafe schlägt?\nMähdrescher',
                'Was trinkt die Chefin?\nLeitungswasser',
                'Vampir in der Verkehrskontrolle.\n"Haben Sie was getrunken?"\n"Ja, zwei Radler."',
                'Wie nennt man jemanden, der DIN A4 Blätter scannt?\nScandinavier',
                'Wie nennt man einen Europäer aus Lettland?\nEuropalette',
                'Hab nem Hipster ins Bein geschossen\nJetzt hopster',
                'Wie viel wiegt ein Influencer?\nEin Instagramm',
                'Was ist gelb und kann nicht schwimmen?\nEin Bagger\nUnd warum nicht?\nHat nur einen Arm',
                'Was hat ein Mann ohne Beine?\nErdnüsse',
                'Welcher Vogel hat Darth Vader auf denn Kopf geschissen?\nDer Star wars',
                'Wie heißt ein Veganer Russe?\nMooskauer',
                'Was ist der Unterschied zwischen Grießbrei und einem Epileptiker?\nDer Grießbrei liegt in Zucker und Zimt, der Epileptiker liegt im Zimmer und zuckt.',
                'Was macht ein Clown im Büro?\nFaxen',
                'Was ist grūn und nuschelt im Gurkensalat?\nDill Schweiger',
                'Was ist die Vergangenheitsform von Tomate? Passierte Tomate',
                'Gehören abgetriebene Babys eigentlich auch zu den entfernen Verwandten?',
                'Kommt ein Dachdecker in ne Bar\nDa sagt der Barkeeper: "Der geht aufs Haus!"',
                'Was spricht man in der Sauna? Schwitzerdeutsch.',
                'Was ist grün und wird auf Knopfdruck rot?\nEin Frosch im Mixer',
                'Was ist weiß und fliegt über die Wiese?\nBiene Majo',
                'Warum trinken Veganer kein Leitungswasser?\nWeil es aus dem Hahn kommt']
        emojis = [':laughing:', ':smile:', ':joy:', ':sob:', ':rofl:']
        msg = f'{random.choice(emojis)} {random.choice(puns)}'
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(fun(bot))
