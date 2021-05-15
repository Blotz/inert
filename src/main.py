from discord.ext import commands
from discord import Intents
import os
import sys
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not loaded")

from sql.prefix import SqlClass

# prefix
sql = SqlClass()
def get_prefix(client, message): return sql.get_prefix(message.guild.id)[0][0]
# add discord bot perms
intents = Intents.default()
# create the client
client = commands.Bot(command_prefix=get_prefix, intents=intents)

# loads all cogs
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')


# prints when bot has started up
@client.event
async def on_ready():
    guilds = client.guilds
    guilds = [guild.id for guild in guilds]

    db_guilds = sql.get_guilds()
    db_guilds = [db_guilds[0] for db_guilds in db_guilds]

    lst = []
    for guild in guilds:
        if guild not in db_guilds:
            lst.append(guild)

    sql.add_guilds(lst, ".")

    lst = []
    for db_guild in db_guilds:
        if db_guild not in guilds:
            lst.append(db_guild)

    sql.remove_guilds(lst)
    print("bot ready")


@client.event
async def on_guild_join(guild):
    sql.add_guild(guild.id, ".")


@client.event
async def on_guild_remove(guild):
    sql.remove_guild(guild.id)


client.run(os.getenv("TOKEN"))
