from time import time
import logging
from discord.ext import commands
from sql.prefix import SqlClass
log = logging.getLogger(__name__)


class System(commands.Cog, name='System commands'):
    """
    system commands
    """

    def __init__(self, client: object):
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

    @commands.command()
    async def ping(self, ctx: object):
        """
        : works out latency of bot
        """
        t1 = time()
        msg = await ctx.send('`pong`')
        t2 = time()
        delay = t2 - t1
        await msg.edit(
            content=f'`Pong! Latency is {round(delay * 1000)}ms. API Latency is {round(self.client.latency * 1000)}ms`')

    # Loading and unloading of cogs for testing
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: object, cog: str):
        """
        : loads a category of commands
        """
        print(f'loading {cog}...')
        self.client.load_extension(f'commands.{cog}')
        await ctx.send(f'`successfully loaded {cog}`')
        print('success!')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: object, cog: str):
        """
        : unloads a category of commands
        """
        print(f'unloading {cog}...')
        self.client.unload_extension(f'commands.{cog}')
        await ctx.send(f'`successfully unloaded {cog}`')
        print('success!')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: object, cog: str):
        """
        : reloads a category of commands
        """
        print(f'reloading {cog}...')
        self.client.unload_extension(f'commands.{cog}')
        self.client.load_extension(f'commands.{cog}')
        await ctx.send(f'`successfully reloaded {cog}`')
        print('success!')

    # Loading and unloading of cogs Error handling
    @load.error
    async def load_error(self, ctx: object, error: object):
        # error if cog doesnt exist
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: cog has not been loaded`')

        # error if user is not bot owner/insufficient perms
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send('`ERROR: insufficient perms to run this command`')
        print('failure!')

    @unload.error
    async def unload_error(self, ctx: object, error: object):
        # error if cog doesnt exist
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: cog has not been unloaded`')

        # error if user is not bot owner/insufficient perms
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send('`ERROR: insufficient perms to run this command`')
        print('failure!')

    @reload.error
    async def reload_error(self, ctx: object, error: object):
        # error if cog doesnt exist
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: cog has not been reloaded`')

        # error if user is not bot owner/insufficient perms
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send('`ERROR: insufficient perms to run this command`')
        print('failure!')


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(System(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
