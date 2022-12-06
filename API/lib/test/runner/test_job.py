import jenkins

from lib.mongo.connection import MongoConnection
from lib.runner.job import Job

import json
import unittest
from unittest.mock import patch

class TestJob(unittest.TestCase):

    def db_setup(self, host_domain):
        mongo = MongoConnection()
        self.user = mongo.db.users.insert_one({"email": "testemail@email.com", "password": "testpassword"}).inserted_id
        self.ext_acc = mongo.db.external_accounts.insert_one({"user": self.user, "username": "aaron", "host_domain": host_domain}).inserted_id
        
    def test_submit(self):
        self.db_setup("mygitlab.com")

        with patch("jenkins.Jenkins") as mock:
            jenkins = mock.return_value
            jenkins.create_job.return_value = None
            jenkins.get_job_info.return_value = {"nextBuildNumber": 1}

            git_url = "https://mygitlab.com/project/name.git"

            job = Job(self.user, self.ext_acc, git_url)
            job_entry_id, build_entry_id = job.submit()

            self.assertNotEqual(None, job_entry_id)
            self.assertNotEqual(None, build_entry_id)


if __name__ == "__main__":
    unittest.main()