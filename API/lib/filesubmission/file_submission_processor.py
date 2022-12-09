import json


from lib.runner.job import Job
from lib.mongo.connection import MongoConnection

class FileSubmissionProcessor:
    def process_file_submission(self, username):

        mongo = MongoConnection()
        user = mongo.db.users.find_one({"_id": username})

        if user is None:
            return "User not found", 401

        job = Job(user["_id"], None, None, user["email"])

        return "", 200
