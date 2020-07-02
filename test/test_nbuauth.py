import unittest

from nbupy import NbuAuthorizationApi
import test_configuration

# Here you can overwrite the global configuration of the test
URL = ''
USER = ''
PASSWORD = ''
VERIFY = ''
DOMAIN_NAME = ''
DOMAIN_TYPE = ''
VERSION = ''
# Read the value from general configuration or from this file
URL = URL if URL else test_configuration.URL
USER = USER if USER else test_configuration.USER
PASSWORD = PASSWORD if PASSWORD else test_configuration.PASSWORD
VERIFY = VERIFY if VERIFY else test_configuration.VERIFY
DOMAIN_NAME = DOMAIN_NAME if DOMAIN_NAME else test_configuration.DOMAIN_NAME
DOMAIN_TYPE = DOMAIN_TYPE if DOMAIN_TYPE else test_configuration.DOMAIN_TYPE
VERSION = VERSION if VERSION else test_configuration.VERSION


class TestNbuAuthorizationApi(unittest.TestCase):

    def setUp(self):
        self.nbu = NbuAuthorizationApi(url=URL, user=USER, password=PASSWORD, verify=VERIFY, domain_name=DOMAIN_NAME,
                                       domain_type=DOMAIN_TYPE, version=VERSION)
        self.nbu.login()

    def tearDown(self):
        self.nbu.logout()

    def test_login(self):
        self.assertIsNotNone(self.nbu._token)

    def test_set_api_key(self):
        # TODO
        pass

    def test_get_app_details(self):
        self.app_details = str(self.nbu.get_app_details())
        self.assertRegex(self.app_details, r'.*STARTED.*', msg=None)
        self.assertRegex(self.app_details, r'.*netbackup.*', msg=None)

    def test_get_authorization_context(self):
        self.assertIsNotNone(self.nbu.get_authorization_context())

    def test_get_ping(self):
        self.ping = str(self.nbu.get_ping())
        self.assertRegex(self.ping, r'[0-9]*', msg=None)

    def test_get_tokenkey(self):
        self.assertIsNotNone(self.nbu.get_tokenkey())

    def test_get_user_sessions(self):
        self.assertIsNotNone(self.nbu.get_user_sessions())

    def test_delete_user_sessions(self):
        self.assertIsNotNone(self.nbu.delete_user_sessions())
        # Login back  to run teardown func
        self.nbu.login()


if __name__ == '__main__':
    unittest.main()
