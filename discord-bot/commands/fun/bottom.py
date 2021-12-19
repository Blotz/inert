import logging
from discord.ext import commands
log = logging.getLogger(__name__)

class Bottom(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        self.CHARACTER_VALUES  = {
            200: "🫂",
            50: "💖",
            10: "✨",
            5: "🥺",
            1: ",",
            0: "❤️"}

        self.SECTION_SEPERATOR = '👉👈'

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