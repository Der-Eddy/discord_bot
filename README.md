![Avatar](img/ava.png)
![Slogan](https://i.imgur.com/vfEgGLU.png)
=====================

[![Python3](https://img.shields.io/badge/python-3.6-blue.svg)](https://github.com/Der-Eddy/discord_bot)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/discord_bot/master/LICENSE)
[![Discord Server](https://img.shields.io/badge/Support-Discord%20Server-blue.svg)](https://discord.gg/kPMbPDc)

This is mostly a german discord chat bot made with [discord.py](https://github.com/Rapptz/discord.py).  
If you are looking for a python discord bot to host for yourself, you should rather take a look at [Red Bot](https://github.com/Twentysix26/Red-DiscordBot). Shinobu is only meant to be run on my own server.

Features
-------------
- [x] Admin & Mod commands  
- [x] Fun commands
- [x] Useless anime commands
- [x] Moderation commands
- [x] Reaction images (Giphy.com)
- [x] Logging of channel messages into a file
- [ ] Upload to Imgur


Eine Auflistung aller Befehle gibt es unter `:help` (Standardpräfix)

![help command](https://i.imgur.com/ntYi4I2.png)


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

In `games.py` kann man die Titel der "Playing-" Rotation:

    __games__ = [
        'with Eddy-Senpai',
        'with Neko-chan',
        'with Cats',
        'try :help',
        'try :status',
        'DARK SOULS IV',
        'with Atom.io',
        'with Python',
        'HuniePop',
        'Crush Crush',
        'try :neko',
        'try :kawaii',
        'with async',
        'with Karen-chan',
        'with Rara-chan',
        'Dota 3'
    ]
    __gamesTimer__ = 10 * 60

Erweiterungen (Cogs) die beim starten aktiviert werden sollen, kann man in `cogs.py` einstellen:

    __cogs__ = [
        'cogs.mod',
        'cogs.admin',
        'cogs.fun',
        'cogs.anime',
        'cogs.utility'
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

    discord.py==0.16.7
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
