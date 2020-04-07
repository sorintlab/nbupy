## nbupy - Veritas Netbackup API Python module

Module to use the API of Veritas Netbackup.

## Supported versions

+ v1.0, v1.1
    - api version 3.0
        + NBU version 8.2

## API

To get started with the API follow the Veritas [guide](https://sort.veritas.com/public/documents/nbu/8.2/windowsandunix/productguides/html/getting-started/).

For the detailed documentation of the API connect to your master node at `https://<master node>/api-docs/index.html`.

## Class

The class `NbuApiConnector` does have a very simple constructor

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

The URL is expected to be in the form `http(s)://<ip>:<port>/<api path>/`.

The `_token` and `_session` attributes will be filled by the `login()` method, and will be used for all subsequent API calls.

You also have a `set_api_key` method to set the token (that will be used in all the following requests) without calling the login.

To use it:

    >>> import nbuapi
    >>> nbu = nbuapi.NbuApiConnector('https://127.0.0.1:1556/netbackup/', 'admin', 'password', False)
    >>> sep.login()
    >>> sep.get_all_jobs()
    {'data': [{'links': {'self': {'href': '/admin/jobs/371'}, 'file-lists': {'href': ....

Or with the `__enter__` and `__exit__` methods:

    >>> import nbuapi
    >>> with nbuapi.NbuApiConnector('https://127.0.0.1:1556/netbackup/', 'admin', 'password', False) as nbu:
    ...     print(sep.get_all_jobs())
    ...
    {'data': [{'links': {'self': {'href': '/admin/jobs/371'}, 'file-lists': {'href': ....

#### Version

The api version value is needed to create the `Accept` header value which looks like this: `application/vnd.netbackup+json;version=<major>.<minor>`

With `DEFAULT_API_VERSION = '3.0'` and `SUPPORTED_API_VERSIONS = ['3.0']`.

I plan to add here the new supported versions of the API.

#### No login methods

These methods doesn't require any authentication

 - get_app_details()
 - get_ping()
 - get_tokenkey()

#### NOTE

The type of the values passed to the functions are not checked.
