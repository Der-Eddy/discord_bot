import discord.ext.test as dpytest
from main import ShinobuBot
import pytest


@pytest.mark.asyncio
async def test_bot():
    bot = ShinobuBot()
    dpytest.configure(bot)

    # Load any extensions/cogs you want to in here
    bot_channel = 165174405222236161
    channel = bot.get_channel(bot_channel)
    await channel.send("Test Message")
    dpytest.verify_message("Test Message")

    await dpytest.message(":about")
    dpytest.verify_message("[Expected help output]")