from discord.ext import commands
import discord

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def poll(self, ctx, *, args: str = ' ') -> None:
        """
        Normal poll. Does {title} [option] [option] and "Foo Bar"
        :param ctx:
        :param args:
        :return:
        """
        if not self.reg.match(args):
            await ctx.message.add_reaction('👍')
            await ctx.message.add_reaction('👎')
            await ctx.message.add_reaction('🤷‍♀️')
            return

        args = args.split('[')
        name = args.pop(0)[1:]
        name = name[:name.find('}')]

        args = [arg[:arg.find(']')] for arg in args]  # thanks ritz for this line

        if len(args) > 20:
            await ctx.send(f"bad {ctx.author.name}! thats too much polling >:(")
            return
        elif len(args) == 0:
            await ctx.send(f"bad {ctx.author.name}! thats too little polling >:(")
            return
        elif name == '' or '' in args:
            await ctx.send(f"bad {ctx.author.name}! thats too simplistic polling >:(")
            return

        description = ''
        for count in range(len(args)):
            description += f'{self.pollsigns[count]} {args[count]}\n\n'

        embed = discord.Embed(title=name, color=discord.Color.gold(), description=description)
        msg = await ctx.send(embed=embed)

        # add reactions
        for count in range(len(args)):
            await msg.add_reaction(self.pollsigns[count])