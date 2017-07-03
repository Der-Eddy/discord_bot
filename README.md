![Avatar](img/ava.png)
![Slogan](https://i.imgur.com/vfEgGLU.png)
=====================

[![Python3](https://img.shields.io/badge/python-3.6-blue.svg)](https://github.com/Der-Eddy/discord_bot)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/discord_bot/master/LICENSE)
[![Discord Server](https://img.shields.io/badge/Support-Discord%20Server-blue.svg)](https://discord.gg/kPMbPDc)

This is mostly a german discord chat bot made with [discord.py](https://github.com/Rapptz/discord.py).  
If you are looking for a python discord bot to host for yourself, you should rather take a look at [Red Bot](https://github.com/Twentysix26/Red-DiscordBot). Shinobu is only meant to be run on my own server.

Commands List
-------------
**Info:** Diese Liste gilt für den Standardprefix `:`

### Generic ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:help` | Zeigt eine Liste aller öffentlichen Commands | `:help`, `:help kawaii`

### Forum ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:epvpis`, `:epvp` | Sucht nach einem Benutzernamen auf Elitepvpers | `:epvpis Der-Eddy`
`:epvpverify`, `:verify` | Verifiziert einen Discord Benutzer über Elitepvpers | `:epvpverify`, `:epvpverify Der-Eddy`
`:kokoro`, `:search` | Gibt Informationen über einen Benutzer von kokoro-ko.de aus | `:kokoro`, `:kokoro Eddy`

### Utility ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:status`, `:s`, `:uptime`, `:up` | Listet einige Informationen zum Bot aus | `:status`
`:ping` | Misst die Response Time | `:ping`
`:github` | Verlinkt zu diesem GitHub Repo | `:github`
`:about`, `:info` | Informationen über Shinobu Oshino | `:about`
`:log`, `:archive` | Archiviert den Log des derzeitigen Channels und läd diesen als Attachment hoch | `:log 10`
`:invite` | Verschickt einen Invite für den Server des Bot Autors | `:invite`
`:whois` | Gibt Informationen über einen Benutzer aus | `:whois @Der-Eddy#6508`
`:emoji`, `:e` | Gibt eine vergrößerte Version eines angegebenen Emojis zurück | `:emoji Emilie`
`:emojis`| Gibt alle Emojis aus auf welche der Bot Zugriff hat | `:emojis`
`:server`, `:serverinfo`, `:guild`, `:membercount` | Gibt Informationen über die derzeitge Discord Guild aus | `:server`
`:timer`, `:reminder` | Setzt einen Timer und benachrichtigt dann einen | `:timer 13m Pizza`, `:timer 2h`
`:source`| Zeigt den Quellcode für einen Befehl auf GitHub an | `:source kawaii`
`:commands`| Zeigt an wie oft welcher Command benutzt wurde seit dem letzten Startup | `:commands`
`:role`| Listet alle Benutzer einer Rolle auf | `:role Admins`
`:games`| Zeigt welche Spiele wie oft auf dem Server gerade gespielt werden | `:games`

### Anime ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:kawaii` | Gibt ein zufälliges kawaii Bild aus | `:kawaii`
`:nsfw` | Vergibt die Rolle um auf die NSFW Channel zugreifen zu können. **Nur auf Eddys Server!** | `:nsfw`
`:hello`, `:wave`, `:hi`, `:ohaiyo` | Nonsense gifs zum Hallo sagen | `:hello`
`:nep`, `:nepu`, `:topnep` | Can't stop the Nep | `:nep`
`:pat` | /r/headpats Pat Pat Pat :3 | `:pat @Der-Eddy#6508`

### Fun ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:java`, `:javascript`, `:nodejs`, `:js` | Weil Java != Javscript | `:java`
`:csharp`, `:c++`, `:c#`, `:objective-c` | Wie soll man da überhaupt durchblicken??? | `:csharp`
`:praise` | Praise the sun | `:praise`
`:css` | Counter Strike: Source | `:css`
`:countdown` | It's the final countdown | `:countdown`
`:neko`, `:cat`, `:randomcat` | Zufällige Katzen Bilder nyan~ | `:neko`
`:random`, `:rand` | Gibt eine zufällige Zahl oder Member aus | `:random`, `:random coin`, `:random 6`, `:random 10 20`, `:random user`
`:steinigt` | Monty Python | `:steinigt @Ravenstorm#1191`
`:hype`, `:hypu`, `:train` | HYPE TRAIN CHOO CHOO | `:hype`
`:xkcd` | Zeigt den letzten oder zufääligen XKCD Comic | `:xkcd`, `:xkcd random`
`:reaction`, `:r`, `:addreaction` | Fügt der letzten Nachricht ein Emoji als Reaction hinzu oder einer bestimmten Nachricht | `:reaction ok_hand`, `:reaction sunglasses 247386709505867776`
`:pun`, `:witz`, `:joke` | Weil jeder schlechte Witze mag | `:pun`
`:tags`, `:tag` | Erstellt tags oder gibt diese aus | `:tags new hentai https://youtu.be/tg3rG-e6haw`, `:tags del 2`, `:tags hentai`

### Gwent ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:gwent`, `:gwint`, `:gwentcard`| Gibt Informationen zu einer Gwent Karte aus | `:gwent Decoy`

### Mod ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:purge`, `:prune` | Löscht mehere Nachrichten auf einmal. **MOD ONLY** | `:purge 100`
`:nickname` | Ändert den Server Nickname vom Bot. **ADMIN ONLY** | `:nickname Shinobu`
`:kick` | Kickt ein Mitglied mit einer Begründung. **MOD ONLY** | `:kick @Der-Eddy#6508`, `:kick @Der-Eddy#6508 Spammt Werbung`
`:ban` | Bannt ein Mitglied mit einer Begründung. **MOD ONLY** | `:ban @Der-Eddy#6508`, `:ban @Der-Eddy#6508 Spammt Werbung`
`:unban` | Entbannt ein Mitglied mit einer Begründung. **MOD ONLY** | `:unban 102815825781596160`
`:bans` | Listet aktuell gebannte User auf. **MOD ONLY** | `:bans`
`:removereactions` | Entfernt alle Emoji Reactions von einer Nachricht. **MOD ONLY** | `:removereactions 247386709505867776`

### Admin ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:shutdown`, `:quit` | Schaltet den Bot aus. **BOT OWNER ONLY** | `:shutdown`
`:restart` | Startet den Bot neu. **BOT OWNER ONLY** | `:restart`
`:avatar` | Setzt einen neuen Avatar. **BOT OWNER ONLY** | `:avatar https://i.imgur.com/iJlPa3V.png`
`:changegame`, `:game` | Ändert das derzeit spielende Spiel. **BOT OWNER ONLY** | `:changegame Dark Souls`
`:changestatus` | Ändert den Online Status vom Bot. **BOT OWNER ONLY** | `:changestatus idle`
`:name` | Ändert den globalen Namen vom Bot. **BOT OWNER ONLY** | `:name Shinobu-chan`
`:servers` | Listet die aktuellen verbundenen Server auf. **BOT OWNER ONLY** | `:servers`
`:leaveserver` | Schaltet den Bot aus. **BOT OWNER ONLY** | `:leaveserver 102817255661772800`
`:echo` | Gibt eine Nachricht als Bot auf einem bestimmten Channel aus. **BOT OWNER ONLY** | `:echo 102817255661772800 Ich bin ein Bot!`
`:discriminator` | Gibt Benutzer mit dem jeweiljigen Discriminator zurück. **BOT OWNER ONLY** | `:discriminator 6508`




Requirements
-------------
Ihr benötigt mindestens Python 3.6 + [discord.py](https://github.com/Rapptz/discord.py) für diesen Bot und einen Discord Bot Account (siehe weiter unten).
Zusätzlich wird `pytz` aus [PyPI](https://pypi.python.org/pypi/pytz/2016.6.1) benötigt.


Run
-------------
Entweder ihr startet das Script direkt über `python3 main.py` oder erstellt eine systemd unit, ein Beispiel findet ihr unter `discord.service.example`:

    [Unit]
    Description=Shinobu Discord Bot
    After=multi-user.target
    [Service]
    WorkingDirectory=/home/eddy/discord_bot
    User=eddy
    Group=eddy
    ExecStart=/usr/bin/python3.6 /home/eddy/discord_bot/main.py
    Type=idle
    Restart=on-failure
    RestartSec=15
    TimeoutStartSec=15

    [Install]
    WantedBy=multi-user.target

Nach `/etc/systemd/system/discord.service` kopieren und anpassen. Nicht vergessen die Unit zu starten via `sudo systemctl start discord.service` bzw. Autostart via `sudo systemctl enable discord.service`.

Bot Accounts
-------------
Allgemeine Infos zu Discord Bot Accounts gibt es bei [discordapp.com/developers/](https://discordapp.com/developers/applications/me).  
Einen Bot Account fügt man dann über diesen Link hinzu (CLIENT ID einfügen nicht vergessen):  
`https://discordapp.com/oauth2/authorize?client_id=CLIENTID&scope=bot&permissions=0`


Einstellungen
-------------
Vor dem Start muss im Ordner `config` eine Datei namens `config.py` angelegt werden, ein Beispiel einer solchen gibt es in `config.example.py` zu finden:

    __token__ = 'INSERT BOT TOKEN HERE'
    __prefix__ = ':'
    __botserverid__ = '102817255661772800' #Specifies the serverid from which the server-/modlog should be taken + some other nito features
    __adminid__ = 'YOUR USERID i.e. 102815825781596160'
    __kawaiichannel__ = '207909155556687872' #OPTIONAL specified a channel where the :kawaii commands gets this pinned messages
    __greetmsg__ = 'False' #HARDCODED Enable/Disable greetmsg at the entry channel of __botserverid__
    __selfassignrole__ = 'Blighttown' #OPTIONAL set to a role to be self assign-able
    __discourseAPIKey__ = {'api_key': '9f0be26ea6a4f47dba6c627ee2f5aa139caa29f8b899bc96c3b7b94755a9363f', 'api_username': 'Eddy'} #OPTIONAL Needed for all discourse related commands
    __cookieJar__ = {'loginuuid': 'löaskdjfölkdfa65sdf46a5s4df56e1f23s1df32asd1f5ef1325s11bSJ9.ImRXcWNHeWI98sd5f4s65ef6s31h1fgjdfg6h54sdfasdfcvbcvb2465UrYlRORDYyTWREQThtYjBrcFEzd1wvbXZJRiswdlwvaWc5YkZSdDlMQUYzZEJIeE03SitsTFZhSFh5cGgrcHducXdzYjVMMTU5U0lGenNITitsYmdSSWIremlNU01UeVM5XC9ZaVpLSFBmaEkyU3NsZjQ1MVNDeHBvOGdaWWxGRlhmZ28raTlcL0RTYzlQaUJkc2N1alp4VW00dXJHMkd5UUttTnZQekZPa2Y1aE1qUjdHNVRwNkdyakhtNUtWc3VWYmUySVc0bkUyQ0pSWVMi.b6nMo5Q3hBMLauEsePPVNSdTJ8I5CqbZFDLrrln-oag', 'bbuserid': '5660970', 'bbpassword': '1753ec1889f70aa87845cc5bfd3b4409'} #OPTIONAL Needed for all elitepvpers related commands

In `games.py` kann man die Titel der "Playing-" Rotation anpassen. Platzhalter wie `{servers}` oder `{members}` sind möglich.

    __games__ = [
        'with Eddy-Senpai',
        'with Neko-chan',
        'with Cats',
        'try :help',
        'try :status',
        'with Atom.io',
        'with Python',
        'HuniePop',
        'try :about',
        'try :kawaii',
        'with async',
        'with Karen-chan',
        'with Rara-chan',
        '{servers} Server',
        '{members} Member'
    ]
    __gamesTimer__ = 10 * 60

Erweiterungen (Cogs) die beim starten aktiviert werden sollen, kann man in `cogs.py` einstellen:

    __cogs__ = [
        'cogs.mod',
        'cogs.admin',
        'cogs.fun',
        'cogs.anime',
        'cogs.utility',
        'cogs.forum',
        'cogs.gwent'
        ]


Support
-------------
Gibts auf meinem Discord Server: `https://discord.gg/kPMbPDc`


Troubleshooting
-------------
Sollte z.B. aus irgendeinem Grund die mod.py cog nicht geladen werden, kann der Bot vom Bot Besitzer über `:shutdown_backup` heruntergefahren werden.
Weitere Tipps folgen

Full list of requirements
-------------

    discord.py
    aiohttp
    websockets
    chardet
    pytz
    memory_profiler


License
-------------
    MIT License

    Copyright (c) 2016 - 2017 Eduard Nikoleisen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Versions prior to 0.6.8 used the Unlicense <http://unlicense.org> license.
