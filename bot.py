"""
bot.py

The core of the bot application.
"""

from random import randint
import discord
from discord.ext import commands
import config as conf
import cogs


# =============================================================================
# Setup
# =============================================================================

# Set up intents
intents = discord.Intents.default()
# intents.members = True # whats this?
intents.message_content = True

# Set up bot
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("puff "),
    intents=intents,
    description=conf.BOT_DESCRIPTION,
)


# =============================================================================
# Base functions
# =============================================================================
@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """

    # Hooking up cogs
    await bot.add_cog(cogs.BaseCog(bot))
    await bot.add_cog(cogs.PollsCog(bot))

    if conf.LOAD_AI:
        await bot.add_cog(cogs.AiCog(bot))

    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"discord.py API version: {discord.__version__}")
    print(f"cogs loaded: {list(bot.cogs.keys())}")
    print(f"listening on: {conf.ACTIVE_CHANNELS}")
    print("Ready to drive!")


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the
    prefix.

    :param message: The message that was sent.
    """

    # Ignore messages from this bot
    if message.author == bot.user or message.author.bot:
        return

    # Annoy users, half of the time in other channels
    if (
        message.author.id in conf.FUCK_YOU_USERS
        and message.channel.id not in conf.ACTIVE_CHANNELS
        and randint(1, 100) > 90
    ):
        await message.reply("Fuck your couch!")
        return

    # Process command if in active channels
    if message.channel.id in conf.ACTIVE_CHANNELS:
        await bot.process_commands(message)


bot.run(conf.BOT_SECRET_KEY)
