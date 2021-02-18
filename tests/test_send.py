import discord
import pytest

bot_channel = 165174405222236161

@pytest.mark.asyncio
async def test_message(bot):
    channel = client.get_channel(bot_channel)

    await channel.send("Test Message")

@pytest.mark.asyncio
async def test_embed(bot):
    channel = client.get_channel(bot_channel)

    embed = discord.Embed(title="Test Embed")
    embed.add_field(name="Field 1", value="Lorem ipsum")

    await channel.send(embed=embed)
