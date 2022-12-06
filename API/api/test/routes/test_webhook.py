import unittest
import json

from unittest.mock import patch

from server import app
from lib.mongo.connection import MongoConnection

class TestWebhook(unittest.TestCase):

    def db_setup(self, host_domain):
        mongo = MongoConnection()
        user = mongo.db.users.insert_one({}).inserted_id
        mongo.db.external_accounts.insert_one({"user": user, "username": "aaron", "host_domain": host_domain})

    def setUp(self):
        self.app = app.test_client()
        self.db_setup("mygitlab.com")
    
    def test_trigger_from_webhook(self):
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

            resp = self.app.post("/webhook/trigger", headers=headers, data=json.dumps(webhook_event))

            self.assertEqual(200, resp.status_code)
            self.assertEqual("", resp.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()