import io
import logging
import re
from functools import partial
import aiohttp
import discord
from PIL import Image, ImageColor
from discord.ext import commands

import cppimport.import_hook
from commands.Image import recolor

log = logging.getLogger(__name__)


class ImageEditing(commands.Cog, name='image'):
    """
    Image editing
    """

    def __init__(self, client):
        self.client = client

    @staticmethod
    async def FindImage(ctx: object) -> bytes or None:
        """finds a discord image
        :param ctx:
        :return:
        :return:
        """
        reg = re.compile(r'https?:/.*\.(png|jpg|jpeg|gif|jfif|bmp)')

        if ctx.message.attachments:
            data = await ctx.message.attachments[0].read()
        else:
            async for msg in ctx.channel.history(limit=25):
                # loop through x messages
                file_url = msg.attachments[0].url if msg.attachments else ''

                message_url = reg.search(msg.content)
                message_url = message_url.group(0) if message_url else ''

                # print(file_url, message_url)
                if reg.match(file_url) or message_url:  # self.reg to check for images in links
                    url = file_url if file_url else message_url
                    # found attachment with image file format
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            data = await response.read()
                    break
            else:
                return None
            # opens and converts to correct file type
        img = Image.open(io.BytesIO(data))
        img = img.convert('RGBA')
        width = img.size[0]
        height = img.size[1]
        maxpixels = 2097152
        imgpixels = width * height

        if imgpixels >= maxpixels:
            # If the image is larger than 8mb resizes
            constg = height / width
            width = round((maxpixels / constg) ** 0.5)
            height = round(width * constg)
            img = img.resize((width, height))
            width = img.size[0]
            height = img.size[1]
        return img, width, height

    @staticmethod
    def ProcessRecolor(img, height, width, color: tuple, strength: float):
        """
        Background Recolor Processing
        :param img:
        :param height:
        :param width:
        :param color:
        :param strength:
        :return:
        """
        img = Image.frombytes('RGBA', img.size, recolor.recolor(img.tobytes(), height, width, color[0], color[1], color[2], strength))

        return img

    @commands.command(aliases=['rc', 'recolour'])
    async def recolor(self, ctx: object, color: str = 'yellow', strength: float = 50):
        """
        Recolors above image
        :param ctx:
        :param color:
        :param strength:
        :return Recolored image:
        """
        color = color.lower()
        # Strength and color definitions
        strength /= 100

        addition_colors = {
            'red': (255, 0, 0, 0),
            'orange': (255, 127, 0, 0),
            'yellow': (255, 255, 0, 0),
            'green': (0, 255, 0, 0),
            'blue': (0, 0, 255, 0),
            'purple': (127, 0, 127, 0),
            'r': 'red',
            'o': 'orange',
            'y': 'yellow',
            'g': 'green',
            'b': 'blue',
            'p': 'purple'
        }
        if len(color) == 1:
            color = addition_colors[color]

        if color not in addition_colors:
            if not color.startswith('#'):
                color = '#' + color
            rgb = ImageColor.getrgb(color)
            addition_colors[color] = (rgb[0], rgb[1], rgb[2], 0)

        # finding image
        bot_msg = await ctx.send('`Editing images`')

        img, width, height = await self.FindImage(ctx)
        if img is None:
            return await bot_msg.edit(content='`No image found`')

        await bot_msg.edit(content='`Image found!`')

        async with ctx.typing():  # typing to show code is working
            # runs in parallel to other code to prevent input output blocking
            fn = partial(self.ProcessRecolor, img, height, width, addition_colors[color], strength)
            img = await self.client.loop.run_in_executor(None, fn)

            # Send image to discord without saving to file
            img_bytes_arr = io.BytesIO()
            img.save(img_bytes_arr, format='PNG')
            img_bytes_arr.seek(0)
            f = discord.File(img_bytes_arr, 'recolour.png')

        await ctx.send(f'`{color}@{int(strength * 100)}%`', file=f)
        await bot_msg.delete()

    @recolor.error
    async def _recolor(self, ctx: object, error: object):
        """
        Error output for Recolor
        :param ctx:
        :param error:
        :return:
        """
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: invalid args <color> <percentage>`')
        elif isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR: invalid color`')
        else:
            await ctx.send('`ERROR: something went wrong`')

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


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(ImageEditing(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
