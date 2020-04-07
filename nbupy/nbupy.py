"""
Module to use the API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""

import requests
from requests.compat import urljoin

__version__ = '1.1'

DEFAULT_PAGE_LIMIT = '20'
DEFAULT_API_VERSION = '3.0'
SUPPORTED_API_VERSIONS = ['3.0']


class NbuApiConnector:

    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version=''):
        self._base_api_url = url
        self._user = user
        self._password = password
        self._verify = verify
        self._domain_type = domain_type
        self._domain_name = domain_name
        self._version = version if version and version in SUPPORTED_API_VERSIONS else DEFAULT_API_VERSION
        self._token = None
        self._session = requests.Session()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        pass

    def _perform_request(self, method, url, *args, **kwargs):
        response = method(url=url, *args, **kwargs)
        response.raise_for_status()
        return response

    def _get_api_call(self, uri, headers=None, parameters=None):
        """ hide _perform_request to the GET api calls """
        h = {
            'Accept': 'application/vnd.netbackup+json;version={}'.format(self._version),
            'Authorization': '{}'.format(self._token)
        }
        if headers:
            for header, value in headers.items():
                h[header] = value
        if parameters:
            return self._perform_request(
                method=self._session.get,
                url=urljoin(self._base_api_url, uri),
                verify=self._verify,
                headers=h,
                json=parameters
            ).json()
        else:
            return self._perform_request(
                method=self._session.get,
                url=urljoin(self._base_api_url, uri),
                verify=self._verify,
                headers=h,
            ).json()

    def _get_unauthorized_api_call(self, uri, headers=None):
        """ hide _perform_request to the GET api calls """
        h = {'Accept': 'application/vnd.netbackup+json;version={}'.format(self._version)}
        if headers:
            for header, value in headers.items():
                h[header] = value
        return self._perform_request(
            method=self._session.get,
            url=urljoin(self._base_api_url, uri),
            verify=self._verify,
            headers=h,
        ).json()

    def _post_api_call(self, uri, headers=None, parameters=None):
        """ hide _perform_request to the simple POST api calls """
        h = {
            'Accept': 'application/vnd.netbackup+json;version={}'.format(self._version),
            'Authorization': '{}'.format(self._token)
        }
        if headers:
            for header, value in headers.items():
                h[header] = value
        if parameters:
            return self._perform_request(
                method=self._session.post,
                url=urljoin(self._base_api_url, uri),
                verify=self._verify,
                headers=h,
                json=parameters
            )
        else:
            return self._perform_request(
                method=self._session.post,
                url=urljoin(self._base_api_url, uri),
                verify=self._verify,
                headers=h
            )

    def _paginated_get_request(self, url, element_id='', filters='', sort=''):
        """ Some API GET calls support pagination: they return the values requested in pages and we need to request all
            the pages to get all the elements.
            Here I try to handle this for all the methods that are using this type of call, trying to use less code
            repetition possible.

            - get_call(): builds the query and makes the GET call
            - generate_elements(): loops calling get_call() to retrieve all the elements

            The last part of the method is discriminating between a call to get a single element or to get all the
            elements

            So far it's possible to use it only for API calls that are structured as ../resource/type/resource_id where
            the resource_id is what here is called element_id
        """
        def get_call(url, element_id='', query=None):
            # NOTE so far parameters and custom headers aren't supported
            url = '{}/{}'.format(url, element_id) if element_id else url
            if query:
                url = url[:-1] if url[len(url) - 1] == '/' else url
                url += '?'
                url += requests.utils.quote('&'.join(['{}={}'.format(q, v) for q, v in query.items()]), safe='=&')
            return self._get_api_call(url)

        def generate_elements(query, url):
            page_offset = ''
            more = True
            while more:
                if page_offset: query['page[offset]'] = page_offset
                resp = get_call(url=url, query=query)
                if 'links' in resp:
                    if 'next' in resp['links']:
                        page_offset = resp['meta']['pagination']['next']
                    if resp['meta']['pagination']['page'] + 1 == resp['meta']['pagination']['pages']:
                        more = False
                yield resp['data'] if 'data' in resp else []

        if element_id:
            return get_call(url, element_id)
        else:
            query = {'page[limit]': DEFAULT_PAGE_LIMIT}
            if filters: query['filter'] = filters
            if sort: query['sort'] = sort
            elements = {'data': []}
            for job_list in generate_elements(query, url):
                elements['data'] = elements['data'] + job_list
            return elements

    # NETBACKUP AUTHENTICATION API

    def login(self):
        resp = self._perform_request(
            method=self._session.post,
            url=urljoin(self._base_api_url, 'login'),
            verify=self._verify,
            headers={'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version)},
            json={
                'userName': self._user,
                'password': self._password,
                'domainType': '',
                'domainName': ''
            },
        )
        self._token = resp.json()['token']

    def logout(self):
        self._perform_request(
            method=self._session.post,
            url=urljoin(self._base_api_url, 'logout'),
            verify=self._verify,
            headers={
                'Accept': 'application/vnd.netbackup+json;version={}'.format(self._version),
                'Authorization': '{}'.format(self._token)
            }
        )
        self._token = None

    def set_api_key(self, api_key):
        self._token = api_key

    def get_app_details(self):
        return self._get_unauthorized_api_call('appdetails')

    def get_authorization_context(self):
        return self._get_api_call('authorization-context')

    def get_ping(self):
        h = {
            'X-NetBackup-API-Version': DEFAULT_API_VERSION,
            'Accept': 'text/vnd.netbackup+plain;version={}'.format(self._version)
        }
        return self._get_unauthorized_api_call('ping', headers=h)

    def get_tokenkey(self):
        h = {'Accept': 'text/vnd.netbackup+html;version={}'.format(self._version)}
        return self._perform_request(
            method=self._session.get,
            url=urljoin(self._base_api_url, 'tokenkey'),
            verify=self._verify,
            headers=h,
        ).content

    def get_user_sessions(self):
        return self._get_api_call('user-sessions')

    def delete_user_sessions(self):
        return self._perform_request(
            method=self._session.delete,
            url=urljoin(self._base_api_url, 'user-sessions'),
            verify=self._verify,
            headers={'Authorization': '{}'.format(self._token)},
        ).content

    # NETBACKUP ADMINISTRATOR API

    def get_jobs(self, jobId='', filters='', sort='-startTime'):
        """
        If jobId is present, returns only that job, else returns all
        """
        return self._paginated_get_request(url='admin/jobs/', element_id=jobId, filters=filters, sort=sort)

    def delete_job(self, jobId, reason=''):
        return self._perform_request(
            method=self._session.delete,
            url=urljoin(self._base_api_url, 'admin/jobs/{}'.format(jobId)),
            verify=self._verify,
            headers={
                'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version),
                'X-NetBackup-Audit-Reason': reason,
                'Authorization': '{}'.format(self._token)
            },
        )

    # NETBACKUP CONFIGURATION API

    def get_policies(self, policyName=None):
        uri = 'config/policies/{}'.format(policyName) if policyName else 'config/policies/'
        return self._get_api_call(uri)

    def create_policy(self, policyRequest, reason='', generic='true'):
        return self._post_api_call(
            'config/policies/',
            {
                'X-NetBackup-Audit-Reason': reason,
                'X-NetBackup-Policy-Use-Generic-Schema': generic,
                'Content-Type': 'application/vnd.netbackup+json;version={}'.format(self._version)
            },
            parameters=policyRequest
        )

    def delete_policy(self, policyName, reason=''):
        return self._perform_request(
            method=self._session.delete,
            url=urljoin(self._base_api_url, 'config/policies/{}'.format(policyName)),
            verify=self._verify,
            headers={
                'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version),
                'Authorization': '{}'.format(self._token)
            },
        )

    # NETBACKUP STORAGE API

    def create_storage_server(self, storageServer):
        return self._post_api_call(
            'storage/storage-servers',
            {'Content-Type': 'application/vnd.netbackup+json;version={}'.format(self._version)},
            parameters=storageServer
        )

    def delete_storage_server(self, storageServer):
        return self._perform_request(
            method=self._session.delete,
            url=urljoin(self._base_api_url, 'storage/storage-servers/{}'.format(storageServer)),
            verify=self._verify,
            headers={
                'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version),
                'Authorization': '{}'.format(self._token)
            },
        )

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
        return self._perform_request(
            method=self._session.delete,
            url=urljoin(self._base_api_url, 'storage/disk-pools/{}'.format(diskPoolId)),
            verify=self._verify,
            headers={
                'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version),
                'Authorization': '{}'.format(self._token)
            },
        )

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
        return self._perform_request(
            method=self._session.delete,
            url=urljoin(self._base_api_url, 'storage/storage-units/{}'.format(storageUnitName)),
            verify=self._verify,
            headers={
                'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version),
                'Authorization': '{}'.format(self._token)
            },
        )
