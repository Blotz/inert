from discord.ext import commands
from sql.prefix import SqlClass

class SetPrefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sql = SqlClass()
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):
        """
        update prefix for the discord server
        """
        self.sql.change_prefix(ctx.guild.id, prefix)
        await ctx.send(f"Updated prefix to: {prefix}")
