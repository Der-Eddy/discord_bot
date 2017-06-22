try:
    from config.config import __token__, __prefix__, __adminid__, __kawaiichannel__, __botlogchannel__, __botserverid__, __greetmsg__, __selfassignrole__, __cookieJar__, __discourseAPIKey__
except ImportError:
    #Heorku stuff
    import os
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __botserverid__ = os.environ.get('DISCORD_BOTSERVERID')
    __adminid__ = os.environ.get('DISCORD_ADMINID')
    __kawaiichannel__ = os.environ.get('DISCORD_KAWAIICHANNEL')
    __botlogchannel__ = os.environ.get('DISCORD_BOTLOGCHANNEL')
    __greetmsg__ = os.environ.get('DISCORD_GREETMSG')
    __selfassignrole__ = os.environ.get('DISCORD_SELFASSIGNROLE')
    __cookieJar__ = os.environ.get('DISCORD_COOKIEJAR')
    __discourseAPIKey__ = os.environ.get('DISCORD_DISCOURSEAPIKEY')

from config.games import __games__, __gamesTimer__
from config.cogs import __cogs__
from config.blacklist import __blacklist__
