import traceback
import logging
from discord.ext import commands
from sql.customcommand import SqlClass

log = logging.getLogger(__name__)
sql = SqlClass()


def is_private_command():
    async def predicate(ctx):
        guild_id = sql.get_command_guild(ctx.command.name)
        if guild_id:
            return ctx.guild.id == sql.get_command_guild(ctx.command.name)[0][0]
        return False

    return commands.check(predicate)


def main(client, command_name, response):
    class Commandtemplate(commands.Cog, name='Custom commands'):
        def __init__(self, client, response):
            self.client = client
            self.command_name = command_name
            self.response = response
            self.sql = SqlClass()

        @commands.command(name=command_name)
        @is_private_command()
        async def custom_command(self, ctx, *args):
            f"""
            {self.sql.get_description(ctx.guild.id, self.command_name)[0][0]}
            """
            print(args)
            await ctx.send(self.response)

        @custom_command.error
        async def _custom_command(self, ctx: object, error: object):
            if not isinstance(error, commands.errors.CheckFailure):
                traceback.print_exc()

    client.add_cog(Commandtemplate(client, response))


class Customcommand(commands.Cog, name='Custom commands'):
    """
    Custom commands
    """

    def __init__(self, client):
        self.client = client

    @commands.group(aliases=["cc"], no_pm=True)
    async def customcommand(self, ctx):
        """Custom command management"""
        if ctx.invoke_subcommand is None:
            ctx.send("not how you use command")

    @customcommand.command(name="add")
    async def cc_add(self, ctx, *, args):
        """Create custom command"""

    @customcommand.command(name="edit")
    async def cc_edit(self, ctx, command_name, option, new_value):
        """Edit custom command"""

    @customcommand.command(name="remove", aliases=["rm"])
    async def cc_remove(self, ctx, command_name):
        """Remove custom command"""

    @customcommand.command(name="list", aliases=["ls"])
    async def cc_list(self, ctx):
        """Lists all custom commands"""

    @commands.command()
    async def ac(self, ctx, command_name, *, response):
        print(response)
        sql.add_command(ctx.guild.id, command_name)
        main(self.client, command_name, response)
        await ctx.send("work")

    @commands.command()
    async def uc(self, ctx, command_name):
        sql.remove_command(ctx.guild.id, command_name)
        self.client.remove_command(command_name)
        await ctx.send("work")


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(Customcommand(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
