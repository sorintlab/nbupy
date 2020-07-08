import logging
from .nbupy import NbuApiConnector
from .nbuauth import NbuAuthorizationApi
from .nbuadmin import NbuAdministratorApi
from .nbuconf import NbuConfigurationApi
from .nbustorage import NbuStorageApi

__version__ = '2.1'

logging.getLogger(__name__).addHandler(logging.NullHandler())

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
except:
    pass
