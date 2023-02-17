"""
bot.py
"""

from random import randint
import discord
from discord.ext import commands
from polls import PollManager


# =============================================================================
# Base functions
# =============================================================================
ACTIVE_CHANNELS = [
]
BOT_NAME = "Puff's Polls"
BOT_DESCRIPTION = "For conducting polls among friends, and a driving test if you are ready."

# Sets up poll bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('puff '),
    intents=intents,
    description=BOT_DESCRIPTION
)
polls = PollManager()


# =============================================================================
# Base functions
# =============================================================================
@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    print(f'Logged in as {bot.user.name}')
    print(f'discord.py API version: {discord.__version__}')
    print(f'listening on channels: {ACTIVE_CHANNELS}')
    print('Ready to drive!')

    for channel_id in ACTIVE_CHANNELS:
        channel = bot.get_channel(channel_id)

        await channel.send("Ready to drive!")


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the
    prefix.

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return

    if message.channel.id in ACTIVE_CHANNELS:
        await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User) -> None:
    """
    The code in this event is executed every time someone adds a reaction to a message.

    :param reaction: The reaction that was added
    :param user: The user that added the reaction.
    """
    poll = polls.get_poll(reaction.message.id)

    if poll:
        poll.vote(user.id, reaction.emoji)
        await reaction.message.remove_reaction(reaction.emoji, user)


# =============================================================================
# Commands
# =============================================================================
@bot.command(name='create', help='Create a poll')
async def create_poll(context: commands.Context, *args) -> None:
    """
    The create command was executed.
    """
    await polls.create_poll(context, *args)


@bot.command(name='list', help='List polls')
async def list_polls(context: commands.Context) -> None:
    """
    The list command was executed.
    """
    await polls.list_polls(context)


@bot.command(name='d20', help='Roll the dice')
async def d_20(context: commands.Context) -> None:
    """
    The d20 command was executed.
    """
    roll = randint(1, 20)
    text = f'Your roll is: {roll}'
    if roll == 20:
        text += '\nGod damn!'
    elif roll == 1:
        text += '\nThings aren\'t lookin up'
    await context.send(text)


bot.run(BOT_SECRET_KEY)
