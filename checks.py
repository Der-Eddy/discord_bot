from discord.ext import commands
import discord.utils
import loadconfig

# Internal Checks
def _check_is_owner(msg):
    return msg.author.id == loadconfig.__adminid__

def _check_permissions(ctx, permissions_needed):
    msg = ctx.message
    if _check_is_owner(msg):
        return True
    permission = msg.channel.permissions_for(msg.author)
    return getattr(permission, permissions_needed, False)

def _check_is_bot_server(msg):
    return msg.guild.id == loadconfig.__botserverid__

# Actual functions for the descorators
def is_bot_owner():
    return commands.check(lambda ctx: _check_is_owner(ctx.message))

def is_administrator():
    def predicate(ctx):
        return _check_permissions(ctx, 'administrator')
    return commands.check(predicate)

def is_administrator_or_owner():
    def predicate(ctx):
        return _check_permissions(ctx, 'administrator') or commands.check(lambda ctx: _check_is_owner(ctx.message))
    return commands.check(predicate)

def has_permissions(perms):
    def predicate(ctx):
        return _check_permissions(ctx, perms)
    return commands.check(predicate)

def is_bot_server():
    #This is needed for commands/events exclusive for the server of the bot owner
    return commands.check(lambda ctx: _check_is_bot_server(ctx.message))
