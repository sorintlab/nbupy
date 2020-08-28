"""
Module to use the API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""

from . import nbuadmin, nbuconf, nbustorage


class NbuApiConnector(nbuadmin.NbuAdministratorApi, nbuconf.NbuConfigurationApi,
                      nbustorage.NbuStorageApi):
    """ General connector that inherits all the methods from the other classes """
    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version='', timeout=0):
        super().__init__(url, user, password, verify, domain_name, domain_type, version)
