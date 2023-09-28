"""
base_cog.py
"""

from random import randint
from discord.ext import commands


class BaseCog(commands.Cog):
    """
    Basic Commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", help="lfg!")
    async def roll(self, context: commands.Context, dice: str) -> None:
        """
        The roll command was executed.
        """
        try:
            rolls, limit = map(int, dice.split("d"))
        except ValueError:
            await context.send("Format has to be in NdN!")
            return

        result = ", ".join(str(randint(1, limit)) for r in range(rolls))
        await context.send(result)

    @commands.command(name="d20", help="Roll the dice")
    async def d_20(self, context: commands.Context) -> None:
        """
        The d20 command was executed.
        """

        current_roll = randint(1, 20)
        text = f"Your roll is: {current_roll}"

        if current_roll == 20:
            text += "\nGod damn!"
        elif current_roll == 1:
            text += "\nThings aren't lookin up"

        await context.send(text)

        # for channel_id in conf.ACTIVE_CHANNELS:

    #     channel = bot.get_channel(channel_id)

    #     if conf.PURGE_MESSAGES_ON_LOAD:
    #         await channel.purge()

    #     await channel.send("Ready to drive!")
