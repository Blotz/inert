# Logging module
import logging
# Importing subcommands
from .anonpoll import AnonPoll
from .poll import Poll

log = logging.getLogger(__name__)


class PollCatagory(AnonPoll, Poll, name=__name__[9:]):
    """
    Polling commands
    """

    def __init__(self, client):
        self.client = client
        AnonPoll.__init__(self, client)
        Poll.__init__(self, client)

def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(PollCatagory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')

