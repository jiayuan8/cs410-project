import unittest
from unittest.mock import patch

import json

from lib.test.helpers.mock_request import MockRequest
from lib.mongo.connection import MongoConnection
from lib.webhook.webhook_processor import WebhookProcessor

class TestWebhookProcessor(unittest.TestCase):

    def db_setup(self, host_domain):
        mongo = MongoConnection()
        user = mongo.db.users.insert_one({}).inserted_id
        mongo.db.external_accounts.insert_one({"user": user, "username": "aaron", "host_domain": host_domain})

    def test_process_gitlab_webhook(self):
        self.db_setup("mygitlab.com")

        headers = {"X-Gitlab-Event": "Push Hook"}
        webhook_event = {
            "user_username": "aaron",
            "project": {
                "git_http_url": "https://mygitlab.com/project/name.git",
            }
        }

        with patch("jenkins.Jenkins") as mock:
            jenkins = mock.return_value
            jenkins.create_job.return_value = None
            jenkins.get_job_info.return_value = {"nextBuildNumber": 1}

            request = MockRequest(headers, webhook_event)
            processor = WebhookProcessor()
            msg, code = processor.process_gitlab_webhook(request)

            self.assertEqual("", msg)
            self.assertEqual(200, code)

    def test_process_github_webhook(self):
        self.db_setup("mygithub.com")

        headers = {"X-GitHub-Event": "push"}
        webhook_event = {
            "sender": {
                "login": "aaron",
            },
            "repository": {
                "clone_url": "https://mygithub.com/aaron/name.git",
            }
        }

        with patch("jenkins.Jenkins") as mock:
            jenkins = mock.return_value
            jenkins.create_job.return_value = None
            jenkins.get_job_info.return_value = {"nextBuildNumber": 1}

            request = MockRequest(headers, webhook_event)
            processor = WebhookProcessor()
            msg, code = processor.process_github_webhook(request)

            self.assertEqual("", msg)
            self.assertEqual(200, code)


if __name__ == "__main__":
    unittest.main()