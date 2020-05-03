import os

configFile = os.path.join('.', 'config', 'config.py')

if os.path.isfile(configFile):
    try:
        from config.config import __token__
    except ImportError:
        raise Exception('__token__ variable MUST be set ')
    try:
        from config.config import __prefix__
    except ImportError:
        __prefix__ = ':'
    try:
        from config.config import __botserverid__
    except ImportError:
        __botserverid__ = 0
    try:
        from config.config import __greetmsg__
    except ImportError:
        __greetmsg__ = ''
    try:
        from config.config import __leavemsg__
    except ImportError:
        __leavemsg__ = ''
    try:
        from config.config import __kawaiichannel__
    except ImportError:
        __kawaiichannel__ = 0
else:
    #Fallback for Heroku or Docker environments
    __token__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')
    __botserverid__ = int(os.environ.get('DISCORD_BOTSERVERID'))
    __kawaiichannel__ = int(os.environ.get('DISCORD_KAWAIICHANNEL'))
    __greetmsg__ = os.environ.get('DISCORD_GREETMSG')
    

from config.games import __games__, __gamesTimer__
from config.cogs import __cogs__
from config.blacklist import __blacklist__
