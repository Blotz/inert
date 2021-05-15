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

print(bool(os.getenv("DEBUG")))
DEBUG: bool = bool(os.getenv("DEBUG", False))
TOKEN: str = os.getenv("TOKEN")
REDDIT_ID: str = os.getenv("REDDIT_ID")
REDDIT_SECRET: str = os.getenv("REDDIT_SECRET")

# Debug Mode Setup
if DEBUG is True:
    # Set Logger Level
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARN)
    logger = logging.getLogger("apscheduler.scheduler:Scheduler")
    logger.setLevel(logging.WARN)
    log.info("Debug Mode Enabled")
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.ERROR)
    logger = logging.getLogger("apscheduler.scheduler:Scheduler")
    logger.setLevel(logging.ERROR)

# Check for token and exit if not exists
if TOKEN is None:
    log.error("Discord API token not set")
    exit()
elif REDDIT_ID is None:
    log.error("REDDIT ID not set")
    exit()
elif REDDIT_SECRET is None:
    log.error("REDDIT SECRET not set")
    exit()
