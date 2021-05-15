import random
import logging
import discord
from discord.ext import commands
log = logging.getLogger(__name__)


class Fun(commands.Cog, name='Fun'):
    """
    Full of lots of fun commands
    """

    def __init__(self, client):
        self.client = client
        self.CHARACTER_VALUES = CHARACTER_VALUES = {
            200: "🫂",
            50: "💖",
            10: "✨",
            5: "🥺",
            1: ",",
            0: "❤️"}

        self.SECTION_SEPERATOR = '👉👈'

    @commands.command(aliases=['hugs'])
    async def hug(self, ctx, target: discord.Member = None):
        """Provides hugs!
        """
        hug_urls = ["https://imgur.com/gvC4K6u", "https://imgur.com/9RGBOLa", "https://imgur.com/ZRGpg8P",
                    "https://imgur.com/7APfwfg", "https://imgur.com/xTJdcbg", "https://imgur.com/D1bJQWL",
                    "https://imgur.com/3AB9LXN", "https://imgur.com/xwogdA8", "https://imgur.com/3aSRyez",
                    "https://imgur.com/OMtbHom", "https://imgur.com/XALtUs4", "https://imgur.com/EIfimk8",
                    "https://imgur.com/BEG77iA", "https://imgur.com/qxeXsRr", "https://imgur.com/osZF2GM",
                    "https://imgur.com/PqotrGa", "https://imgur.com/sYCVhZ1", "https://imgur.com/ItZk2E7",
                    "https://imgur.com/ng81k8S", "https://imgur.com/4bGa09O"]

        if target is None:
            await ctx.send(f"*hugs back*")
        elif target == ctx.author:
            await ctx.send("https://imgur.com/xTJdcbg")
        else:
            hug_result = random.choice(hug_urls)

            author_name = ctx.author.name if ctx.author.nick is None else ctx.author.nick

            await ctx.send(f"A hug from {author_name}!")
            await ctx.send(f"{hug_result}")

    @commands.group('bottomify', pass_context=True)
    async def bottomify(self, ctx):
        """
        This command bottomifies the input of your text!
        Thanks to the bottom foundation for this code
        Taken from https://gi/bottom-software-foundation/bottom-py/blob/main/bottom.py
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("bottom")

    @bottomify.command(name='bottomify', aliases=['bottom', "butt"])
    async def bottom_encode(self, ctx, *, text):
        """
        Encodes to Bottom Speak
        """
        out = bytearray()

        for char in text.encode():
            while char != 0:
                for value, emoji in self.CHARACTER_VALUES.items():
                    if char >= value:
                        char -= value
                        out += emoji.encode()
                        break

            out += self.SECTION_SEPERATOR.encode()

        await ctx.send(f"`{out.decode('utf-8')}`")

    @bottomify.command(name='decode')
    async def bottom_decode(self, ctx, text):
        """
        Decodes from Bottom Speak
        """
        out = bytearray()

        text = text[1:-1]
        text = text.strip()
        if self.SECTION_SEPERATOR and text.endswith(self.SECTION_SEPERATOR):
            text = text[:-len(self.SECTION_SEPERATOR)]
        else:
            text = text[:]

        if not all(c in self.CHARACTER_VALUES.values() for c in text.replace(self.SECTION_SEPERATOR, '')):
            raise TypeError(f'Invalid bottom text: {text}')

        for char in text.split(self.SECTION_SEPERATOR):
            rev_mapping = {v: k for k, v in self.CHARACTER_VALUES.items()}

            sub = 0
            for emoji in char:
                sub += rev_mapping[emoji]

            out += sub.to_bytes(1, 'big')

        await ctx.send(out.decode())

    @commands.command()
    async def uwu(self, ctx, *, message):
        """
        UwU-ifies any message you give it... no matter the size owo
        """
        uwus = ['UwU', 'xwx', 'DwD', 'ÚwÚ', 'uwu', '☆w☆', '✧w✧',
                '♥w♥', '︠uw ︠u', '(uwu)', 'OwO', 'owo', 'Owo', 'owO', '( ͡° ͜ʖ ͡°)']
        res = message.replace("r", "w").replace(
            "l", "w").replace("L", "W").replace("R", "W")
        res = res.replace("the ", "da ").replace(
            "The ", "Da ").replace("THE ", "DA ")
        res = res.replace("th", "d").replace("TH", "D")
        res = res.replace("\n", " " + random.choice(uwus) + "\n")
        # and send one "as" da usew who invoked da command ÚwÚ
        await ctx.send(f"{res + ' ' + random.choice(uwus)}")


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(Fun(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
