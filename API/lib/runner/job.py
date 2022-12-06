from flask_login import current_user

from lib.runner.jenkins_srv import JenkinsSrv
from lib.mongo.connection import MongoConnection

from bson.objectid import ObjectId
import re
import time
import json

class Job:

    def __init__(self, user_id, external_account_id, git_url, user_email):
        self.user_id = user_id
        self.external_account_id = external_account_id
        self.git_url = git_url
        self.user_email = user_email
        self.jenkins_srv = JenkinsSrv()
        self.jenkins_srv.connect_to_jenkins()

    def submit(self):
        job_entry_id = None
        build_no = 1

        mongo = MongoConnection()

        job_entry = mongo.db.jobs.find_one({"user": self.user_id, "git_url": self.git_url})

        if job_entry == None:
            job_entry_id = mongo.db.jobs.insert_one({"user": self.user_id, "git_url": self.git_url}).inserted_id
            job_config = self._generate_job_config()
            self.jenkins_srv.srv.create_job(str(job_entry_id), job_config)
        else:
            job_entry_id = job_entry["_id"]
            try:
                build_no = self.jenkins_srv.srv.get_job_info(str(job_entry_id))["nextBuildNumber"] 
            except: #something went wrong during the previous job, so it wasn't actually created
                del_jobs = { "user": self.user_id, "git_url":self.git_url }
                mongo.db.jobs.delete_many(del_jobs)
                job_entry_id = mongo.db.jobs.insert_one({"user": self.user_id, "git_url": self.git_url}).inserted_id
                job_config = self._generate_job_config()
                self.jenkins_srv.srv.create_job(str(job_entry_id), job_config)


        
        self.jenkins_srv.srv.build_job(str(job_entry_id))

        build_entry = {
            "job": job_entry_id,
            "user": self.user_id,
            "build_number": build_no,
            "created_at": time.time(),
            "status": "QUEUED",
            "time_elapsed": 0
        }

        build_entry_id = mongo.db.builds.insert_one(build_entry).inserted_id

        return job_entry_id, build_entry_id

    def _generate_job_config(self):
        credential_id = str(self.external_account_id)
        template_config = self._load_template_config()

        config = re.sub(
            "<url>GIT_URL_HERE</url>",
            f"<url>{self.git_url}</url>",
            template_config,
        )

        config = re.sub(
            "<credentialsId>GIT_API_TOKEN_HERE</credentialsId>",
            f"<credentialsId>{credential_id}</credentialsId>",
            config,
        )

        print(self.user_email,credential_id,flush=True)

        return config

    def _load_template_config(self):
        fileshare_config = json.loads(open("fileshare_config.json").read())
        fileshare_name = fileshare_config["fileshare_name"]
        fileshare_password = fileshare_config["fileshare_password"]

        return f"""
<project>
    <actions/>
    <description/>
    <keepDependencies>false</keepDependencies>
    <properties>
        <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.12">
            <gitLabConnection/>
        </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
    </properties>
    <scm class="hudson.plugins.git.GitSCM" plugin="git@3.12.0">
        <configVersion>2</configVersion>
        <userRemoteConfigs>
            <hudson.plugins.git.UserRemoteConfig>
                <url>GIT_URL_HERE</url>
                <credentialsId>GIT_API_TOKEN_HERE</credentialsId>
            </hudson.plugins.git.UserRemoteConfig>
        </userRemoteConfigs>
        <branches>
            <hudson.plugins.git.BranchSpec>
                <name>*/master</name>
            </hudson.plugins.git.BranchSpec>
            <hudson.plugins.git.BranchSpec>
                <name>*/main</name>
            </hudson.plugins.git.BranchSpec>
        </branches>
        <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
        <submoduleCfg class="list"/>
        <extensions/>
    </scm>
    <assignedNode>ubuntu</assignedNode>                                
    <canRoam>false</canRoam>
    <disabled>false</disabled>
    <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
    <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
    <triggers/>
    <concurrentBuild>false</concurrentBuild>
    <builders>
        <hudson.tasks.Shell>
            <command>sudo mkdir /azure || true</command>
        </hudson.tasks.Shell>

        <hudson.tasks.Shell>
            <command>sudo echo {self.user_email} | dd of=username.txt</command>
        </hudson.tasks.Shell>
         <hudson.tasks.Shell>
            <command>sudo umount /azure || true</command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>sudo mount -t cifs //{fileshare_name}.file.core.windows.net/default-fileshare /azure -o vers=3.0,username={fileshare_name},password={fileshare_password},dir_mode=0755,file_mode=0755 || true</command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
         <command>sudo apt --yes install python2-minimal</command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py</command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>sudo python2 get-pip.py</command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>python2 -u /azure/master/executor.py</command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>
        """
