![Avatar](img/ava.png)
![Slogan](https://i.imgur.com/vfEgGLU.png)
=====================

[![Python3](https://img.shields.io/badge/python-3.7-blue.svg)](https://github.com/Der-Eddy/discord_bot)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/discord_bot/master/LICENSE)
[![Discord Server](https://img.shields.io/badge/Support-Discord%20Server-blue.svg)](https://discord.gg/kPMbPDc)
![Docker](https://github.com/Der-Eddy/discord_bot/workflows/Docker/badge.svg)

**ATTENTION: This bot uses the new version of [discord.py v1.0+](https://github.com/Rapptz/discord.py/tree/rewrite), if you want to use my bot with the old legacy discord.py version check out the [legacy branch](https://github.com/Der-Eddy/discord_bot/tree/0.18.10-legacy).**
This is mostly a german discord chat bot made with [discord.py v1.0+](https://github.com/Rapptz/discord.py).  
If you are looking for a python discord bot to host for yourself, you should rather take a look at [Red Bot](https://github.com/Twentysix26/Red-DiscordBot) if you want a highly customizable self-hosted python bot. Shinobu is only meant to be run on my own server.

Using `pip install discord.py` will install the latest discord.py version.

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

### Utility ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:status`, `:s`, `:uptime`, `:up` | Listet einige Informationen zum Bot aus | `:status`
`:ping` | Misst die Response Time | `:ping`
`:github` | Verlinkt zu diesem GitHub Repo | `:github`
`:about`, `:info` | Informationen über Shinobu Oshino | `:about`
`:log`, `:archive` | Archiviert den Log des derzeitigen Channels und läd diesen als Attachment hoch | `:log 10`
`:invite` | Erstellt einen Invite Link für den derzeitigen Channel | `:invite`
`:whois` | Gibt Informationen über einen Benutzer aus | `:whois @Der-Eddy#6508`
`:emoji`, `:e` | Gibt eine vergrößerte Version eines angegebenen Emojis zurück | `:emoji Emilie`
`:emojis`| Gibt alle Emojis aus auf welche der Bot Zugriff hat | `:emojis`
`:server`, `:serverinfo`, `:guild`, `:membercount` | Gibt Informationen über die derzeitge Discord Guild aus | `:server`
`:timer`, `:reminder` | Setzt einen Timer und benachrichtigt einen dann | `:timer 13m Pizza`, `:timer 2h`
`:source`| Zeigt den Quellcode für einen Befehl auf GitHub an | `:source kawaii`
`:commands`| Zeigt an wie oft welcher Command benutzt wurde seit dem letzten Startup | `:commands`
`:roleUsers`| Listet alle Benutzer einer Rolle auf | `:roleUsers Admins`
`:games` | Zeigt welche Spiele wie oft auf dem Server gerade gespielt werden | `:games`
`:spoiler` | Erstellt ein GIF Bild welches beim Hover einen Spoiler Text anzeigt | `:spoiler`
`:ranks`, `:rank`, `:role`, `:roles` | Auflistung aller Ränge oder beitritt eines bestimmten Ranges | `:ranks`, `:ranks Python'`
`:addvote` | Fügt Emotes als Reactions hinzu für Abstimmungen/Umfragen | `:addvotes`, `:vote`, `:votes`

### Anime ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:kawaii` | Gibt ein zufälliges kawaii Bild aus | `:kawaii`
`:nsfw` | Vergibt die Rolle um auf die NSFW Channel zugreifen zu können. **Nur auf Eddys Server!** | `:nsfw`
`:hello`, `:wave`, `:hi`, `:ohaiyo` | Nonsense gifs zum Hallo sagen | `:hello`
`:nep`, `:nepu`, `:topnep` | Can't stop the Nep | `:nep`
`:pat` | /r/headpats Pat Pat Pat :3 | `:pat @Der-Eddy#6508`
`:ratewaifu`, `:rate`, `:waifu` | Bewertet deine Waifu | `:ratewaifu Shinobu`
`:anime`, `:anilist` | Sucht auf AniList.co nach einem Anime und gibt die Basis-Informationen zurück | `:anime Mushishi`
`:manga` | Sucht auf AniList.co nach einem Manga und gibt die Basis-Informationen zurück | `:manga Air Gear`
`:saucenao`, `:sauce`, `:iqdb` | Versucht die Quelle eines Anime Bildes zu finden | `:saucenao https://i.imgur.com/nmnVtgs.jpg`

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
`:xkcd` | Zeigt den letzten oder zufälligen XKCD Comic | `:xkcd`, `:xkcd random`
`:reaction`, `:r`, `:addreaction` | Fügt der letzten Nachricht ein Emoji als Reaction hinzu oder einer bestimmten Nachricht | `:reaction ok_hand`, `:reaction sunglasses 247386709505867776`
`:pun`, `:witz`, `:joke` | Weil jeder schlechte Witze mag | `:pun`
`:tags`, `:tag` | Erstellt tags oder gibt diese aus | `:tags new hentai https://youtu.be/tg3rG-e6haw`, `:tags del 2`, `:tags hentai`

### Mod ###

Command und Aliases | Beschreibung | Nutzung
----------------|--------------|-------
`:purge`, `:prune` | Löscht mehere Nachrichten auf einmal. **MOD ONLY** | `:purge 100`
`:kick` | Kickt ein Mitglied mit einer Begründung. **MOD ONLY** | `:kick @Der-Eddy#6508`, `:kick @Der-Eddy#6508 Spammt Werbung`
`:ban` | Bannt ein Mitglied mit einer Begründung. **MOD ONLY** | `:ban @Der-Eddy#6508`, `:ban @Der-Eddy#6508 Spammt Werbung`
`:unban` | Entbannt ein Mitglied mit einer Begründung. **MOD ONLY** | `:unban 102815825781596160`
`:bans` | Listet aktuell gebannte User auf. **MOD ONLY** | `:bans`
`:removereactions` | Entfernt alle Emoji Reactions von einer Nachricht. **MOD ONLY** | `:removereactions 247386709505867776`
`:permissions` | Listet alle Rechte des Bots auf. **ADMIN OR BOT OWNER ONLY** | `:permissions`
`:hierarchy` | Listet die Rollen-Hierarchie des derzeitigen Servers auf. **ADMIN OR BOT OWNER ONLY** | `:hierarchy`
`:setrank`, `:setrole`, `:sr` | Vergibt einen Rang an einem Benutzer. **MOD ONLY** | `:setrole @Der-Eddy#6508 Member`
`:rmrank`, `:rmrole`, `:removerole`, `:removerank` | Entfernt einen Rang von einem Benutzer. **MOD ONLY** | `:rmrole @Der-Eddy#6508 Member`

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
`:discriminator` | Gibt Benutzer mit dem jeweiligen Discriminator zurück. **BOT OWNER ONLY** | `:discriminator 6508`
`:nickname` | Ändert den Server Nickname vom Bot. **BOT OWNER ONLY** | `:nickname Shinobu`
`:setnickname` | Ändert den Nickname eines Benutzer. **BOT OWNER ONLY** | `:setnickname @Der-Eddy#6508 Shinobu`
`:geninvite` | Generiert einen Invite für einen Server wenn möglich. **BOT OWNER ONLY** | `:geninvite 102817255661772800`


Run (Docker method)
-------------

GitHub Actions erstellt automatisch ein Docker image unter `ghcr.io/der-eddy/shinobu_bot` (AMD64 und ARM64). Unter `docker-compose.examle.yml` findet ihr ein Beispiel wie man dieses einsetzt:

    version: '3.9'

    services:
    discord_bot:
        container_name: discord_bot
        image: ghcr.io/der-eddy/shinobu_bot:latest
        restart: always
        volumes:
        - discord_bot_data:/discord_bot/config
        environment:
        DISCORD_TOKEN: 'INSERT BOT TOKEN HERE'
        DISCORD_PREFIX: ':' #OPTIONAL Prefix for all commands, defaults to colon
        DISCORD_BOTSERVERID: '102817255661772800' #OPTIONAL Specifies the main serverid from which the server-/modlog should be taken + some other nito features
        DISCORD_KAWAIICHANNEL: '207909155556687872' #OPTIONAL specified a channel where the :kawaii commands gets this pinned messages
        DISCORD_GREETMSG: '{emoji} Welcome {member} on my server!' #OPTIONAL sends a greet message to new user in the botserverid system channel
        DISCORD_LEAVEMSG: ':sad: {member} left the server' #OPTIONAL sends a leave message to the botserverid system channel

    volumes:
    discord_bot_data:

Anzumerken ist dass das Docker Image [Googles distroless](https://github.com/GoogleContainerTools/distroless) Python 3.7 Basis benutzt, d.h. das nicht mal eine Shell vorinstalliert ist. Ihr könnt natürlich auch euer eigenes Docker Image anhand der `Dockerfile` selber bauen lassen-

Run (old method)
-------------
Erstellt zuerst ein virtuelles environment für Python über `python3.7 -m venv env` und aktiviert es über `source env/bin/activate` (Linux only). Anschließend könnt ihr alle benötigten Abhängikeiten über `pip install -r requirements.txt` installieren.
(Um aus der virtuellen Umgebung wieder raus zu kommen einfach `deactivate` eintippen)

Anschließend started ihr das Script direkt über `python3 main.py` oder erstellt eine systemd service unit, ein Beispiel findet ihr unter `discord.service.example`:

    [Unit]
    Description=Shinobu Discord Bot
    After=multi-user.target
    [Service]
    WorkingDirectory=/home/eddy/discord_bot
    Environment="PYTHONHASHSEED=0"
    User=eddy
    Group=eddy
    ExecStart=/usr/bin/python3 /home/eddy/discord_bot/main.py
    Type=idle
    Restart=on-failure
    RestartSec=15
    TimeoutStartSec=15

    [Install]
    WantedBy=multi-user.target

Nach `/etc/systemd/system/discord.service` kopieren und anpassen. Nicht vergessen die Unit zu starten via `sudo systemctl start discord.service` bzw. Autostart via `sudo systemctl enable discord.service`.


Einstellungen
-------------
Vor dem Start muss im Ordner `config` eine Datei namens `config.py` angelegt werden, ein Beispiel einer solchen gibt es in `config.example.py` zu finden:

    __token__ = 'INSERT BOT TOKEN HERE'
    __prefix__ = ':' #OPTIONAL Prefix for all commands, defaults to colon
    __botserverid__ = 102817255661772800 #OPTIONAL Specifies the main serverid from which the server-/modlog should be taken + some other nito features
    __kawaiichannel__ = 207909155556687872 #OPTIONAL specified a channel where the :kawaii commands gets this pinned messages
    __greetmsg__ = '{emoji} Welcome {member} on my server!' #OPTIONAL sends a greet message to new user in the botserverid system channel
    __leavemsg__ = ':sad: {member} left the server' #OPTIONAL sends a leave message to the botserverid system channel


In `games.py` kann man die Titel der "Playing-" Rotation anpassen. Platzhalter wie `{servers}` oder `{members}` sind möglich.

    __games__ = [
        (discord.ActivityType.playing, 'with Eddy-Senpai'),
        (discord.ActivityType.playing, 'with Cats'),
        (discord.ActivityType.playing, 'try :help'),
        (discord.ActivityType.playing, 'try :about'),
        (discord.ActivityType.playing, 'with VS Code'),
        (discord.ActivityType.playing, 'with Python'),
        (discord.ActivityType.playing, 'with async'),
        (discord.ActivityType.playing, 'with Karen-chan'),
        (discord.ActivityType.playing, 'with Hinata-chan'),
        (discord.ActivityType.playing, 'with Eduard Laser'),
        (discord.ActivityType.watching, 'over {guilds} Server'),
        (discord.ActivityType.watching, 'over {members} Members'),
        (discord.ActivityType.watching, 'Trash Animes'),
        (discord.ActivityType.watching, 'you right now'),
        (discord.ActivityType.watching, 'Hentai'),
        (discord.ActivityType.listening, 'Podcasts')
    ]
    __gamesTimer__ = 2 * 60 #2 minutes

Erweiterungen (Cogs) die beim starten aktiviert werden sollen, kann man in `cogs.py` einstellen:

    __cogs__ = [
        'cogs.admin',
        'cogs.mod',
        'cogs.fun',
        'cogs.anime',
        'cogs.utility',
        'cogs.help'
        ]


Support
-------------
Gibts auf meinem Discord Server: `https://discord.gg/kPMbPDc`


Troubleshooting
-------------
Sollte z.B. aus irgendeinem Grund die mod.py cog nicht geladen werden, kann der Bot vom Bot Besitzer über `:shutdown_backup` heruntergefahren werden.
Weitere Tipps folgen

List of requirements
-------------

    python>=3.7.0
    discord.py
    aiohttp
    websockets
    pytz
    pillow

For a pinned version check `requirements.txt`


License
-------------
    MIT License

    Copyright (c) 2016 Eduard Nikoleisen

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
