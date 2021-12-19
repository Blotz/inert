import random
import logging
import discord
from discord.ext import commands
log = logging.getLogger(__name__)

class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client

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

