import jenkins
import json
import requests
import urllib.parse

class JenkinsSrv:

    def __init__(self):
        self.srv = None

    def connect_to_jenkins(self):
        jenkins_config = self._load_jenkins_config()
        server = jenkins.Jenkins(
            jenkins_config["url"],
            username=jenkins_config["username"],
            password=jenkins_config["password"],
        )
        self.srv = server
        print("in jenkins")
        return self.srv

    def create_credential_for_api_key(self, credential_id, username, api_key):
        """We use the external_account_id from mongo as the credential id in jenkins since it's a unique pk"""
        jenkins_config = self._load_jenkins_config()
        s = requests.Session()
        crumb_url = f"http://{jenkins_config['username']}:{jenkins_config['password']}@{jenkins_config['jenkins_server']}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,%22:%22,//crumb)"
        crumb = s.get(crumb_url).text.split('Jenkins-Crumb:')[1] #hardcoding response key here, probably not great
        url = f"http://{jenkins_config['username']}:{jenkins_config['password']}@{jenkins_config['jenkins_server']}/credentials/store/system/domain/_/createCredentials"
        headers = {"Content-type": "application/x-www-form-urlencoded","Jenkins-Crumb":crumb}
        data = {
            "json": json.dumps({
                "": "0",
                "credentials": {
                    "scope": "GLOBAL",
                    "id": credential_id,
                    "username": username,
                    "password": api_key,
                    "description": "API key for linked account",
                    "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
                } 
            })
        }
        resp = s.post(url, headers=headers, data=data)
        
        return resp.status_code == 200,resp.text

    def get_build_logs(self, job_id, build_number):
        jenkins_config = self._load_jenkins_config()
        url = f"http://{jenkins_config['username']}:{jenkins_config['password']}@{jenkins_config['jenkins_server']}/job/{job_id}/{build_number}/consoleText"
        resp = requests.get(url)
        return resp.text

    def _load_jenkins_config(self):
        with open("jenkins_config.json") as f:
            jenkins_config = json.loads(f.read())
            f.close()

        return jenkins_config
