from discord.ext import commands
import logging

import discord

log = logging.getLogger(__name__)

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    def isAllowed(user: discord.Member, target: discord.Member) -> bool:
        """Checks whether the user is able to use this command on the member"""
        return user.top_role > target.top_role
    
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a user from the server with an optional reason"""
        if self.isAllowed(ctx.author, member) is False:
            # Return some sort of error output
            return
        
        # Kicks the user
        await member.kick(reason=reason)

        # Outputting to logs
        # needs an sql refactor :deadeyes:
