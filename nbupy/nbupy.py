"""
Module to use the API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""

from .nbuadmin import NbuAdministratorApi
from .nbuconf import NbuConfigurationApi
from .nbustorage import NbuStorageApi


class NbuApiConnector(NbuAdministratorApi, NbuConfigurationApi, NbuStorageApi):
    """ General connector that inherits all the methods from the other classes """
    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version=''):
        super(NbuApiConnector, self).__init__(url, user, password, verify, domain_name, domain_type, version)
