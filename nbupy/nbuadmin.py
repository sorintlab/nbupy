"""
Module to use the Administrator API of Veritas Netbackup

by Sorint https://sorint.it

License GPLv3
"""

from . import nbuauth


class NbuAdministratorApi(nbuauth.NbuAuthorizationApi):
    """ Here are implemented the methods for the administrator API of netbackup """

    def __init__(self, url, user, password, verify, domain_name='', domain_type='', version=''):
        super().__init__(url, user, password, verify, domain_name, domain_type, version)

    # NETBACKUP ADMINISTRATOR API

    def get_jobs(self, jobId='', filters='', sort='-startTime'):
        """
        If jobId is present, returns only that job, else returns all
        """
        return self._paginated_get_request(url='admin/jobs/', element_id=jobId, filters=filters, sort=sort)

    def delete_job(self, jobId, reason=''):
        headers = {'X-NetBackup-Audit-Reason': reason}
        return self._delete_api_call('admin/jobs/{}'.format(jobId), headers=headers)
