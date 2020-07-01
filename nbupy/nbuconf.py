"""
Module to use the Configuration API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""

from . import nbuauth


class NbuConfigurationApi(nbuauth.NbuAuthorizationApi):
    """ Here are implemented the methods for the configuration API of netbackup """

    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version=''):
        super().__init__(url, user, password, verify, domain_name, domain_type, version)

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
        return self._delete_api_call('config/policies/{}'.format(policyName))
