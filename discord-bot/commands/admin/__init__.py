# Logging module
import logging
# Importing subcommands
from .setprefix import SetPrefix
from .role import Role
from .moderation import Moderation

log = logging.getLogger(__name__)


class AdminCatagory(SetPrefix, Role, Moderation, name=__name__[9:]):
    """
    Administation commands
    """

    def __init__(self, client):
        self.client = client
        SetPrefix.__init__(self, client)
        Role.__init__(self, client)
        Moderation.__init__(self, client)


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(AdminCatagory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')

