![Avatar](img/ava.png)
![Slogan](https://i.imgur.com/vfEgGLU.png)
=====================

[![Python3](https://img.shields.io/badge/python-3.5-blue.svg)](https://github.com/Der-Eddy/discord_bot)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/discord_bot/master/LICENSE)
[![Trello Board](https://img.shields.io/badge/Management-Trello%20Board-blue.svg)](https://trello.com/b/Kh8nfuBE/discord-bot-shinobu-chan)
[![Discord Server](https://img.shields.io/badge/Support-Discord%20Server-blue.svg)](https://discord.gg/kPMbPDc)

This is mostly a german discord chat bot made with [discord.py](https://github.com/Rapptz/discord.py).  

Features
-------------
- [x] Admin & Mod commands  
- [x] Fun commands
- [x] Useless anime commands
- [x] Heroku Support
- [x] Moderation/Server Log
- [x] Message on GitHub Commit
- [x] Reaction images (Giphy.com + own database)
- [ ] Upload to Imgur

More Details can be found at our [Trello Board](https://trello.com/b/Kh8nfuBE/discord-bot-shinobu-chan)!


Eine Auflistung aller Befehle gibt es unter `:help` (Standardpräfix)

![help command](https://i.imgur.com/5lyZEZh.png)


Run & Requirements
-------------
Ihr benötigt mindestens Python 3.5 + [discord.py](https://github.com/Rapptz/discord.py) für diesen Bot und einen Discord Bot Account (siehe weiter unten).
Vor dem Start muss im selben Ordner wie `main.py` eine Datei namens `config.py` angelegt werden, ein Beispiel einer solchen gibt es in `config.example.py` zu finden:

    __token__ = 'INSERT BOT TOKEN HERE'
    __prefix__ = ':'
    __botserverid__ = '102817255661772800' #Specifies the serverid from which the server-/modlog should be taken
    __adminid__ = 'YOUR USERID i.e. 102815825781596160'
    __adminrole__ = 'Administrator'
    __modrole__ = 'Moderators'
    __kawaiichannel__ = '207909155556687872' #OPTIONAL specified a channel where the :kawaii commands gets this pinned messages
    __botlogchannel__ = '165175306561388545' #Channel for the server-/modlog, should be probably a channel on the same server as __botserverid__
    __github__ = 'False' #OPTIONAL logs new commits of this bot into a specific channel, sorry hardcoded!
    __greetmsg__ = 'False' #HARDCODED Enable/Disable greetmsg at the entry channel of __botserverid__
    __selfassignrole__ = 'Blighttown' #OPTIONAL set to a role to be self assign-able


Zusätzlich wird `pytz` aus [PyPI](https://pypi.python.org/pypi/pytz/2016.6.1) benötigt.


Support
-------------
Gibts auf meinem Discord Server: `https://discord.gg/kPMbPDc`


Bot Accounts
-------------
Allgemeine Infos zu Discord Bot Accounts gibt es bei [discordapp.com/developers/](https://discordapp.com/developers/applications/me).  
Einen Bot Account fügt man dann über diesen Link hinzu (CLIENT ID einfügen nicht vergessen):  
`https://discordapp.com/oauth2/authorize?client_id=CLIENTID&scope=bot&permissions=0`


Full list of requirements
-------------

    discord.py==0.11.0
    aiohttp
    websockets
    chardet
    pytz


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

Versions prior to 0.6.8 used the Unlicense <http://unlicense.org> license.
