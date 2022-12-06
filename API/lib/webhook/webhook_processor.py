import json

from lib.runner.job import Job
from lib.mongo.connection import MongoConnection
from lib.webhook import webhook_common


class WebhookProcessor:

    def process_gitlab_webhook(self, request):
        event_body = json.loads(request.data)

        gitlab_username = event_body["user_username"]
        git_http_url = event_body["project"]["git_http_url"]

        return self._process_webhook(gitlab_username, git_http_url)

    def process_github_webhook(self, request):
        event_body = json.loads(request.data)

        github_username = event_body["sender"]["login"]
        git_http_url = event_body["repository"]["clone_url"]

        return self._process_webhook(github_username, git_http_url)

    def _process_webhook(self, username, git_http_url):
        host_domain = webhook_common.get_host_domain_from_url(git_http_url)

        mongo = MongoConnection()
        account = mongo.db.external_accounts.find_one({"username": username, "host_domain": host_domain})

        if account == None:
            return "Github account not found", 401

        user = mongo.db.users.find_one({"_id": account["user"]})
        
        if user == None:
            return "User not found", 401

        job = Job(user["_id"], account["_id"], git_http_url, user["email"])
        job.submit()

        return "", 200
