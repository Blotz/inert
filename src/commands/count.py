import logging
from functools import partial
import discord
import requests
from discord.ext import commands
from praw import Reddit
from settings import (REDDIT_SECRET, REDDIT_ID)
from sql.count import SqlClass
log = logging.getLogger(__name__)

class Count(commands.Cog, name='counting'):
    """
    Counts different subreddits
    """

    def __init__(self, client):
        self.client = client
        self.reddit = Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent='Yellow Beetlejuice Discord bot'
        )
        self.sql = SqlClass()

        red_sub = ("DSRRed", "red")
        orange_sub = ("EternalOrange", "orange")
        yellow_sub = ("YellowOnlineUnion", "yellow")
        green_sub = ("TheGreenArmy", "green")
        blue_sub = ("AzureEmpire", "blue")
        purple_sub = ("PurpleImperium", "purple")

        self.sub = {
            "red": red_sub,
            "rd": red_sub,
            "r": red_sub,

            "orange": orange_sub,
            "ornge": orange_sub,
            "orang": orange_sub,
            "o": orange_sub,

            "yellow": yellow_sub,
            "yelow": yellow_sub,
            "y": yellow_sub,

            "green": green_sub,
            "grn": green_sub,
            "g": green_sub,

            "blue": blue_sub,
            "blu": blue_sub,
            "b": blue_sub,

            "purple": purple_sub,
            "purp": purple_sub,
            "p": purple_sub,

            "pink": green_sub
        }

    def get_hotposts(self, sub: str):
        posts = []
        stickies = 0
        for submission in self.reddit.subreddit(sub).hot(limit=130):
            if submission.stickied:
                stickies += 1
            posts.append(submission)

        posts = posts[stickies:]
        return posts

    @commands.command(aliases=["c"])
    async def count(self, ctx, col="yellow"):
        """Counts the top 125 posts on a subreddit
        :param ctx:
        :param col: the color of the subreddit
        :return:
        """
        col = col.lower()
        # gets the sub name
        if col not in self.sub.keys():
            await ctx.send('`Sub not found`')
            return
        sub = self.sub[col]
        # sub = ('subname', 'color')

        msg = await ctx.send('Counting...')

        fn = partial(self.get_hotposts, sub[0])
        posts = await self.client.loop.run_in_executor(None, fn)

        # Include only the author names.
        # only green has proper css class names. as green will be using the command the most on their sub, it will be used to verify color
        posts = list(map(lambda a: [a.author.name, a.author_flair_css_class], posts))

        pages = []
        for i in range(0, 5):
            pages.append(posts[i * 25:(i + 1) * 25])
        # [[25 posts], [25 posts], [25 posts], [25 posts], [25 posts]]
        # post = [author_name,author_name,author_name, etc...]

        users = {}
        count = []
        page_count = {
            'red': 0,
            'orange': 0,
            'yellow': 0,
            'green': 0,
            'blue': 0,
            'purple': 0
        }
        for page in pages:
            # page = [author_name, author_name, author_name, etc...]
            # resets values in dict
            page_count = page_count.fromkeys(page_count, 0)

            for author in page:
                # author = 'reddit account name'
                if author[0] in users.keys():
                    # if user has already been seen by the code
                    user_color = users[author[0]]
                    page_count[user_color] += 1
                else:
                    # if the code hasnt seen this user, it checks the database
                    userinfo = self.sql.get_reddit_color(author[0])  # if user color unknown, funct returns empty list
                    if userinfo:
                        user_color = userinfo[0][0]
                    else:
                        # if the user isnt in the database, it checks the api
                        url = f'https://api.flairwars.com/users?RedditUsername={author[0]}'
                        header = {"accept": "application/json"}
                        r = requests.get(url, headers=header)
                        userinfo = r.json()
                        if userinfo:
                            # print(userinfo)
                            user_color = userinfo[0]['FlairwarsColor']
                            self.sql.add_discord_user(userinfo[0]['DiscordMemberID'])
                            self.sql.add_reddit_user(author[0], userinfo[0]['FlairwarsColor'])
                            self.sql.add_reddit_discord(userinfo[0]['DiscordMemberID'], author[0])
                        else:
                            # if flairapi doesnt have it, it will try and parse the information from the posts
                            # this is unreliable and inconsistent. it will only work on green

                            # purple uses alternative css class names which breaks this. hence why im checking for it
                            if (author[1] is not None) and (author[1].lower() in ("red", "orange", "yellow", "green", "blue", "purple")):
                                user_color = author[1].lower()
                                self.sql.add_reddit_user(author[0], user_color)
                            else:
                                user_color = author[0]
                                page_count[user_color] = 0

                    page_count[user_color] += 1
                    users[author[0]] = user_color
            count.append(page_count)
        # count = [{color posts per page},{},{}]

        response = f'**Situation over on {sub[1].capitalize()}**'

        for page in range(0, 5):
            response += f'\n**Page {page + 1}**\n'
            for key in count[page].keys():
                if count[page][key] != 0:
                    response += f'{key} : {str(count[page][key])}\n'.replace("_", "\_").replace("*", "\*").replace("~", "\~")

        await msg.edit(content=response)

    @count.error
    async def _count(self, error, ctx):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: .count yellow`')
        else:
            await ctx.send(f'`ERROR: {type(error), error}`')


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(Count(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
