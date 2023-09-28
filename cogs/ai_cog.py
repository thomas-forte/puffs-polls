"""
ai_cog.py
"""

from discord.ext import commands
import spacy


class AiCog(commands.Cog):
    """
    Basic Commands
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.nlp = spacy.load("en_core_web_lg")

        self.weather_statement = self.nlp("What is the weather in city")

    @commands.command(name="ai", help="Ai assistant")
    async def process_ai(self, context: commands.Context, *args) -> None:
        """
        The ai command was executed.
        """
        user_statement = self.nlp(" ".join(args))

        await context.send(f"{self.weather_statement.similarity(user_statement)}")
