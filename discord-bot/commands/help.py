from discord.ext import commands
import logging
log = logging.getLogger(__name__)


class Help(commands.Cog, name='Help'):
    """
    Help command
    """

    def __init__(self, client):
        client.remove_command("help")
        self.client = client

    @commands.group(name="help", no_pm=True)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None or isinstance(ctx.invoked_subcommand, commands.Group):
            help_str = """```md\n**Categories**"""

            cogs = [[cog_name, cog_object] for cog_name, cog_object in self.client.cogs.items()]

            for i in range(1, len(cogs)):
                cog = cogs[i]
                j = i - 1
                while j >= 0 and cog[0] < cogs[j][0]:
                    cogs[j + 1] = cogs[j]
                    j -= 1
                cogs[j + 1] = cog

            for cog_name, cog_object in cogs:
                help_str += f"\n# {cog_name} \n- {cog_object.description}"

            help_str += "\n\nrun .help command <command> or .help group <group> to get more info```"
            await ctx.send(help_str)

    @help.command(name="command", aliases=['cmd'])
    async def help_command(self, ctx, *, cmd):
        """
        returns info on specific commands
        :param ctx:
        :param cmd:
        :return:
        """
        cmd_object = self.client.get_command(cmd)
        if cmd_object is not None:
            cog_object = cmd_object.cog
            help_str = f"""```md\n**Commands**\n{cog_object.description}"""

            help_str += f"\n\n# {cmd_object.name}"
            if len(cmd_object.aliases) > 0:
                help_str += str(cmd_object.aliases)
            help_str += f"\n- {cmd_object.help}"

            help_str += "\n\nrun .help command <command> or .help group <group> to get more info```"
            await ctx.send(help_str)
        else:
            await ctx.send("```no command found```")

    @help.command(name="category", aliases=['cat', 'group'])
    async def help_group(self, ctx, *, group):
        """
        returns info on a specific group
        :param ctx:
        :param group:
        :return:
        """
        group_cog = self.client.get_cog(group)
        if group_cog is not None:
            cmds = group_cog.get_commands()
            help_str = f"""```md\n**Category**\n{group_cog.description}"""

            # ordering cogs in alphabetical order
            for i in range(1, len(cmds)):
                cmd = cmds[i]
                j = i - 1
                while j >= 0 and cmd.name < cmds[j].name:
                    cmds[j + 1] = cmds[j]
                    j -= 1
                cmds[j + 1] = cmd

            # creating the help output
            for cmd in cmds:
                help_str += f"\n\n# {cmd.name} "
                if len(cmd.aliases) > 0:
                    help_str += str(cmd.aliases)
                help_str += f"\n- {cmd.short_doc}"

            help_str += "\n\nrun .help command <command> or .help group <group> to get more info```"
            await ctx.send(help_str)
        else:
            await ctx.send("```no category found```")


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(Help(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
