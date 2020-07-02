import unittest

from nbupy import NbuAdministratorApi
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


class TestNbuAdministratorApi(unittest.TestCase):

    def setUp(self):
        self.nbu = NbuAdministratorApi(url=URL, user=USER, password=PASSWORD, verify=VERIFY, domain_name=DOMAIN_NAME,
                                       domain_type=DOMAIN_TYPE, version=VERSION)
        self.nbu.login()

    def tearDown(self):
        self.nbu.logout()

    def test_get_jobs(self):
        self.assertIsNotNone(self.nbu.get_jobs())

    def test_delete_jobs(self):
        jobs = self.nbu.get_jobs()
        # Checking response equals to 202
        self.assertRegex(str(self.nbu.delete_job(jobs['data'][0]['attributes']['jobId'])), r'202')


if __name__ == '__main__':
    unittest.main()
