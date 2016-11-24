import discord
from discord.ext import commands
import loadconfig

class roleAssign(discord.Client):
    '''Fügt eine Rolle neuen Benutzern beim joinen des Server hinzu'''

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        if member.server.id == loadconfig.__botserverid__ or True:
            role = discord.utils.get(member.server.roles, name=loadconfig.__selfassignrole__)
            await self.bot.add_roles(member, role)


def setup(bot):
    bot.add_cog(roleAssign(bot))
