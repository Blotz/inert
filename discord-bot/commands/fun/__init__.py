# Logging module
import logging
# Importing subcommands
from .hug import Hug
from .bottom import Bottom
from .uwu import Uwu

log = logging.getLogger(__name__)


class FunCatagory(Hug, Bottom, Uwu, name=__name__[9:]):
    """
    Full of lots of fun commands
    """

    def __init__(self, client):
        self.client = client
        Hug.__init__(self, client)
        Bottom.__init__(self, client)
        Uwu.__init__(self, client)


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(FunCatagory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')

