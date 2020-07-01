"""
Module to use the Storage API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""

from . import nbuauth


class NbuStorageApi(nbuauth.NbuAuthorizationApi):
    """ Here are implemented the methods for the storage API of netbackup """

    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version=''):
        super().__init__(url, user, password, verify, domain_name, domain_type, version)

    # NETBACKUP STORAGE API

    def create_storage_server(self, storageServer):
        return self._post_api_call(
            'storage/storage-servers',
            {'Content-Type': 'application/vnd.netbackup+json;version={}'.format(self._version)},
            parameters=storageServer
        )

    def delete_storage_server(self, storageServer):
        return self._delete_api_call('storage/storage-servers/{}'.format(storageServer))

    def get_disk_volumes(self, storageServerId):
        """
        Here storageServerId is mandatory, so the call will always be the paginated one
        """
        return self._paginated_get_request(url='storage/storage-servers/{}/disk-volumes/'.format(storageServerId))

    def create_disk_pool(self, diskPool):
        return self._post_api_call(
            'storage/disk-pools',
            {'Content-Type': 'application/vnd.netbackup+json;version={}'.format(self._version)},
            parameters=diskPool
        )

    def get_disk_pools(self, diskPoolId=''):
        """
        If diskPoolId is present, returns only that disk pool, else returns all
        """
        return self._paginated_get_request(url='storage/disk-pools', element_id=diskPoolId)

    def delete_disk_pool(self, diskPoolId):
        return self._delete_api_call('storage/disk-pools/{}'.format(diskPoolId))

    def create_storage_unit(self, storageUnit):
        return self._post_api_call(
            'storage/storage-units',
            {'Content-Type': 'application/vnd.netbackup+json;version={}'.format(self._version)},
            parameters=storageUnit
        )

    def get_storage_units(self, storageUnitName=''):
        """
        If storageUnitName is present, returns only that storage unit, else returns all
        """
        return self._paginated_get_request(url='storage/storage-units', element_id=storageUnitName)

    def delete_storage_unit(self, storageUnitName):
        return self._delete_api_call('storage/storage-units/{}'.format(storageUnitName))

