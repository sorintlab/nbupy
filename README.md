## nbupy - Veritas Netbackup API Python module

At Sorint we make an extensive use of Netbackup with our customers and we had the necessity to automate many of the repetitive activities. We started to use the very complete Netbackup API with python and found it very effective. We were missing a standard python client library so we created this.

We think this it is enough simple and easily extensible to automate all of your tasks without any problem.

## Supported versions

+ v2.1.1
    - api version 3.0
        + NBU version 8.2

## API

To get started with the API follow the Veritas [guide](https://sort.veritas.com/public/documents/nbu/8.2/windowsandunix/productguides/html/getting-started/).

For the detailed documentation of the API connect to your master node at `https://<master node>/api-docs/index.html`.

## Install

    python setup.py install

## Class

There are many classes, hierarchically organized.

At the top is `NbuAuthorizationApi` that implements the methods to communicate to the API plus the authorizaiton API calls.
Between these are the `login` and `logout` calls.

This Class is inherited by all the other classes, so they implement the same `__init__` and have the `login` and `logout`, plus their specific methods, example:

    class NbuConfigurationApi(NbuAuthorizationApi)

The class `NbuApiConnector` inherits the methods of all the classes, except for `NbuAuthorizationApi` which is already inherited by the other methods.

### Constructor

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

## Usage

To use it import the class that implements the methods you need:

    >>> from nbupy import NbuAdministratorApi
    >>> nbu = NbuAdministratorApi('https://127.0.0.1:1556/netbackup/', 'admin', 'password', False)
    >>> nbu.login()
    >>> nbu.get_all_jobs()

Or by using NbuApiConnector that implements all the methods:

    >>> from nbupy import NbuApiConnector
    >>> nbu = nbupy.NbuApiConnector('https://127.0.0.1:1556/netbackup/', 'admin', 'password', False)
    >>> nbu.login()
    >>> nbu.get_all_jobs()
    >>> nbu.get_disk_pools()

Using the `with` keyword:

    >>> from nbupy import NbuApiConnector
    >>> with NbuApiConnector('https://127.0.0.1:1556/netbackup/', 'admin', 'password', False) as nbu:
    ...     print(nbu.get_all_jobs())

#### Version

The api version value is needed to create the `Accept` header value which looks like this: `application/vnd.netbackup+json;version=<major>.<minor>`

The variables `DEFAULT_API_VERSION = '3.0'` and `SUPPORTED_API_VERSIONS = ['3.0']` define the default value used in the api (if not defined in the __init__), and all the supported versions.

I plan to add to `SUPPORTED_API_VERSIONS` the new supported versions of the API.

#### NOTE

The type of the values passed to the functions are not checked.

## Contribute

To submit your changes please open a pull request.

## License

GPL-3.0

## Author Information

Sorint.Lab Spain
