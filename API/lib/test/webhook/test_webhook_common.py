import unittest
import json

from lib.test.helpers.mock_request import MockRequest
from lib.webhook import webhook_common


class TestWebhookCommon(unittest.TestCase):

    def test_determine_webhook_source_gitlab(self):
        headers = {"X-Gitlab-Event": "Push Hook"}
        webhook_event = {}

        request = MockRequest(headers, webhook_event)
        source = webhook_common.determine_webhook_source(request)

        self.assertEqual("GITLAB", source)

    def test_determine_webhook_source_github(self):
        headers = {"X-Github-Event": "push"}
        webhook_event = {}

        request = MockRequest(headers, webhook_event)
        source = webhook_common.determine_webhook_source(request)

        self.assertEqual("GITHUB", source)

    def test_determine_webhook_source_none(self):
        headers = {}   
        webhook_event = {}

        request = MockRequest(headers, webhook_event)
        source = webhook_common.determine_webhook_source(request)

        self.assertEqual(None, source)

    def test_get_host_domain_from_url_gitlab(self):
        git_url = "https://mygitlab.com/project/name.git"
        domain = webhook_common.get_host_domain_from_url(git_url)
        self.assertEqual("mygitlab.com", domain)

    def test_get_host_domain_from_url_github(self):
        git_url = "https://mygithub.com/aaron/name.git"
        domain = webhook_common.get_host_domain_from_url(git_url)
        self.assertEqual("mygithub.com", domain)

    def test_get_host_domain_from_url_subdomain(self):
        git_url = "https://lab.textdata.org/project/name.git"
        domain = webhook_common.get_host_domain_from_url(git_url)
        self.assertEqual("lab.textdata.org", domain)


if __name__ == "__main__":
    unittest.main()