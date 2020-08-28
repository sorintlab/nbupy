"""
Module to use the Authentication API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""
import logging

import requests
from requests.compat import urljoin

DEFAULT_PAGE_LIMIT = '20'
DEFAULT_API_VERSION = '3.0'
SUPPORTED_API_VERSIONS = ['3.0']
DEFAULT_TIMEOUT = 20


class NbuAuthorizationApi(object):
    """
        Here are implemented the methods to communicate with the api and the authorization methods.
        This class is inherited by other classes in this package
    """

    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version='', timeout=DEFAULT_TIMEOUT):
        self._base_api_url = url
        self._user = user
        self._password = password
        self._verify = verify
        self._domain_type = domain_type
        self._domain_name = domain_name
        self._version = version if version and version in SUPPORTED_API_VERSIONS else DEFAULT_API_VERSION
        self._token = None
        self._session = requests.Session()
        self.timeout = timeout

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        pass

    def _perform_request(self, method, url, *args, **kwargs):
        logging.debug('call to [{}]'.format(url))
        response = method(url=url, timeout=self.timeout, *args, **kwargs)
        try:
            response.raise_for_status()
        except Exception as e:
            error_info = '' if not response.text else (response.text if response.text[-1] != '\n' else response.text[:-1])
            logging.debug('error info: "{}"'.format(error_info))
            raise e
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

    def _delete_api_call(self, uri, headers=None, parameters=None):
        """ hide _perform_request to the simple DELETE api calls """
        h = {
            'content-type': 'application/vnd.netbackup+json;version={}'.format(self._version),
            'Authorization': '{}'.format(self._token)
        }
        if headers:
            for header, value in headers.items():
                h[header] = value
        if parameters:
            return self._perform_request(
                method=self._session.delete,
                url=urljoin(self._base_api_url, uri),
                verify=self._verify,
                headers=h,
                json=parameters
            )
        else:
            return self._perform_request(
                method=self._session.delete,
                url=urljoin(self._base_api_url, uri),
                verify=self._verify,
                headers=h
            )

    def _paginated_get_request(self, url, element_id='', filters='', sort='', headers=None, parameters=None):
        """ Some API GET calls support pagination: they return the requested values in pages and we need to request all
            the pages to get all the values.
            Here I try to handle this for all the methods that are using this type of call.

            - get_call(): builds the query and makes the GET call
            - generate_elements(): loops calling get_call() to retrieve all the elements

            The last part of the method is discriminating between a call to get a single element or to get all the
            elements

            So far it's possible to use it only for API calls that are structured as ../resource/type/resource_id where
            the resource_id is what here is called element_id
        """
        def get_call(url, element_id='', query=None, headers=None, parameters=None):
            url = '{}/{}'.format(url, element_id) if element_id else url
            if query:
                url = url[:-1] if url[-1] == '/' else url
                url += '?'
                url += requests.utils.quote('&'.join(['{}={}'.format(q, v) for q, v in query.items()]), safe='=&')
            return self._get_api_call(url, headers, parameters)

        def generate_elements(query, url, headers=None, parameters=None):
            page_offset = ''
            more = True
            while more:
                if page_offset: query['page[offset]'] = page_offset
                resp = get_call(url=url, query=query, headers=headers, parameters=parameters)
                if 'links' in resp:
                    if 'next' in resp['links']:
                        page_offset = resp['meta']['pagination']['next']
                    if (resp['meta']['pagination']['page'] + 1 == resp['meta']['pagination']['pages']) or resp['meta']['pagination']['pages'] == 0:
                        more = False
                yield resp['data'] if 'data' in resp else []

        if element_id:
            return get_call(url=url, element_id=element_id, headers=headers, parameters=parameters)
        else:
            query = {'page[limit]': DEFAULT_PAGE_LIMIT}
            if filters: query['filter'] = filters
            if sort: query['sort'] = sort
            elements = {'data': []}
            for job_list in generate_elements(query, url, headers, parameters):
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
