"""
Poll.py
"""

from datetime import datetime, timedelta
from discord.ext import commands


class PollEmoji:
    """
    Helper to convert numbers to emoji and emoji to numbers for polls
    """

    POLL_NUMBER = {
        0: '0️⃣',
        1: '1️⃣',
        2: '2️⃣',
        3: '3️⃣',
        4: '4️⃣',
        5: '5️⃣',
        6: '6️⃣',
        7: '7️⃣',
        8: '8️⃣',
        9: '9️⃣',
        10: '🔟',
    }

    POLL_EMOJI = {}
    for key, val in POLL_NUMBER.items():
        POLL_EMOJI[val] = key

    @staticmethod
    def index_to_emoji(index: int) -> str:
        """
        index -> emoji
        """
        return PollEmoji.POLL_NUMBER.get(index, '🏴‍☠️')

    @staticmethod
    def emoji_to_index(emoji: str) -> int:
        """
        emoji -> index
        """
        return PollEmoji.POLL_NUMBER.get(emoji, -1)


class Poll:
    """
    Representation of a poll.
    """

    def __init__(self, author_id: int, text: str, options: list[str]) -> None:
        self.author_id = author_id
        self.text = text
        self.options = options
        self.votes = {}

        self.closed: bool = False
        self.end_date: datetime = datetime.now() + timedelta(days=1)

    def __str__(self) -> str:
        return f'{self.text} {self.scores()}'

    def vote(self, user_id: int, emoji: str) -> None:
        """
        Update or cast vote.
        """

        self.votes[user_id] = PollEmoji.emoji_to_index(emoji)

    def scores(self) -> dict[int, int]:
        """
        Build scores
        """

        scores = {}

        for i in range(len(self.options)):
            scores[i] = 0

        for option in self.votes.values():
            s = scores.get(option)
            if s:
                scores[option] += 1

        return scores

    def winner(self) -> str:
        """
        """
        # scores = self.scores()
        # winner = { 0: 0 }
        # for option, score in scores.items():
        #     if score > winner:
        #         winner
        return PollEmoji.index_to_emoji(1)


class PollManager:
    """
    Manages polls and can handle commands.
    """

    def __init__(self) -> None:
        self.polls: dict[int, Poll] = {}

    def get_poll(self, message_id: int) -> Poll | None:
        """
        Looks up poll based on message_id
        """

        return self.polls.get(message_id, None)

    async def create_poll(self, context: commands.Context, *args) -> None:
        """
        Creates a poll.
        """

        raw_text = ' '.join(args).replace(' -option ', ' -o ')
        text = raw_text.split(' -o ', 1)[0]
        raw_options = raw_text.split(' -o ')[1:]
        options: list[str] = [s.strip() for s in raw_options]

        if not text or len(options) < 2:
            await context.send('Bad create command.')
            return

        raw_message = (
            f'Hi @everyone!\n'
            f'{context.author.mention}\'s bitch ass decided it\'s a good time to conduct a poll.\n'
            '\n'
            f'{text}\n'
            '\n'
        )
        count = 0

        for option in options:
            raw_message += f'{PollEmoji.index_to_emoji(count)} {option}\n'
            count += 1

        message = await context.send(raw_message)

        for i in range(len(options)):
            await message.add_reaction(PollEmoji.index_to_emoji(i))

        self.polls[message.id] = Poll(
            author_id=context.author.id,
            text=text,
            options=options
        )

        await context.message.delete()

    async def list_polls(self, context: commands.Context) -> None:
        """
        List all polls.
        """

        raw_message = ''
        count = 1

        for poll in self.polls.values():
            raw_message += f'{count}. {poll}\n'
            count += 1

        if not raw_message:
            raw_message = 'No polls to list.'
        else:
            raw_message = 'Polls found:\n' + raw_message

        await context.send(raw_message)
