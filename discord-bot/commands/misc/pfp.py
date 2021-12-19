import logging
import discord
from discord.ext import commands

log = logging.getLogger()

class Pfp(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['avatar'])
    async def pfp(self, ctx, *, member: discord.Member = None):
        """Gets your pfp or pfp of another
        :param ctx:
        :param member: optional. the user who's pfp you want to see
        :return: embed with pfp
        """
        url = ctx.author.avatar_url if member is None else member.avatar_url
        embed = discord.Embed(color=discord.Color.gold())
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @pfp.error
    async def _pfp(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('`ERROR: member not found`')
        else:
            log.info(error)
