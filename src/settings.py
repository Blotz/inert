"""
Contains all configuration for bot.
All settings should be loaded from enviroment variables.
For development, create a .env file in the package and make sure python-dotenv is installed.
"""

import logging
import os

log = logging.getLogger(__name__)

# Check for python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logging.debug("python-dotenv not loaded. Hope you set your environment variables.")

DEBUG: bool = bool(os.getenv("DEBUG", False))
TOKEN: str = os.getenv("TOKEN")
REDDIT_ID: str = os.getenv("REDDIT_ID")
REDDIT_SECRET: str = os.getenv("REDDIT_SECRET")
DATABASE_TYPE: str = os.getenv("DATABASE_TYPE")

# Debug Mode Setup
__handlers = [logging.FileHandler('logs/discord_bot.log'), logging.StreamHandler()]
__format = '%(asctime)s:%(levelname)s:%(message)s'

if DEBUG is True:
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.DEBUG,
        format=__format,
        handlers=__handlers
    )
    # Set Logger Level
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARN)
    logger = logging.getLogger("apscheduler.scheduler:Scheduler")
    logger.setLevel(logging.WARN)
    log.info("Debug Mode Enabled")
else:
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format=__format,
        handlers=__handlers
    )
    logger = logging.getLogger("discord")
    logger.setLevel(logging.ERROR)
    logger = logging.getLogger("apscheduler.scheduler:Scheduler")
    logger.setLevel(logging.ERROR)

# Check for token and exit if not exists
if TOKEN is None:
    log.error("Discord API token not set")
    exit()
elif REDDIT_ID or REDDIT_SECRET is None:
    log.error("REDDIT ID or SECRET not set")
