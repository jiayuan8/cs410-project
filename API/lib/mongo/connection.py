import json
import os
from pymongo import MongoClient



class MongoConnection:

    def __init__(self):
        self._connect_to_mongo()

    def _connect_to_mongo(self):
        with open("mongo_config.json") as f:
            config = json.loads(f.read())
            f.close()

        env = os.environ["FLASK_ENV"]
        env_config = config[env]
        self.client = MongoClient(env_config["host"])
        self.db = self.client[env_config["db"]]


        # prev_id = { "username": "Jon-LaFlamme" }
        # self.db.external_accounts.delete_many(prev_id)
        # prev_id = {"git_url":"https://github.com/Jon-LaFlamme/MP1_Private.git"}
        # self.db.jobs.delete_many(prev_id)

        # prev_id = { "username": "jongwoojeff" }
        # self.db.external_accounts.delete_many(prev_id)
        # prev_id = {"git_url":"https://github.com/jongwoojeff/MP1_private.git"}
        # self.db.jobs.delete_many(prev_id)

        # prev_id = { "username": "ahmadaldhalaan" }
        # self.db.external_accounts.delete_many(prev_id)
        # prev_id = {"git_url":"https://github.com/ahmadaldhalaan/MP1_private.git"}
        # self.db.jobs.delete_many(prev_id)




        


    def __del__(self):
        self.client.close()