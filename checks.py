from discord.ext import commands
import discord.utils
import loadconfig

# Checks
def _check_is_owner(msg):
    return msg.author.id == loadconfig.__adminid__

def _check_permissions(ctx, permissions_needed):
    msg = ctx.message
    if _check_is_owner(msg):
        return True
    permission = msg.channel.permissions_for(msg.author)
    return getattr(permission, permissions_needed, False)

# Actual functions for the descorators
def is_bot_owner():
    return commands.check(lambda ctx: _check_is_owner(ctx.message))

def is_administrator():
    def predicate(ctx):
        return _check_permissions(ctx, 'administrator')
    return commands.check(predicate)

def has_permissions(perms):
    def predicate(ctx):
        return _check_permissions(ctx, perms)
    return commands.check(predicate)
