"""
polls_cog.py
"""

import discord
from discord.ext import commands
import config as conf
from polls import PollManager


class PollsCog(commands.Cog):
    """
    Basic Commands
    """

    def __init__(self, bot):
        self.bot = bot
        # Sets up poll db
        self.polls = PollManager()

    @commands.Cog.listener
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User) -> None:
        """
        The code in this event is executed every time someone adds a reaction to a message.

        :param reaction: The reaction that was added
        :param user: The user that added the reaction.
        """

        # Ignore reaction if not in active channels
        if reaction.message.channel.id not in conf.ACTIVE_CHANNELS:
            return

        poll = self.polls.get_poll(reaction.message.id)

        if poll:
            poll.vote(user.id, reaction.emoji)
            await reaction.message.remove_reaction(reaction.emoji, user)

    @commands.command(name="create", help="Create a poll")
    async def create_poll(self, context: commands.Context, *args) -> None:
        """
        The create command was executed.
        """

        await self.polls.create_poll(context, *args)

    @commands.command(name="list", help="List polls")
    async def list_polls(self, context: commands.Context) -> None:
        """
        The list command was executed.
        """

        await self.polls.list_polls(context)
