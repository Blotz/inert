import random
import logging
from discord.ext import commands
log = logging.getLogger(__name__)


class Uwu(commands.Cog):
    def __init__(self, client):
        self.client = client

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
