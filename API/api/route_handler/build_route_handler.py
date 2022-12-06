from flask_login import current_user
import jenkins

import lib.github.project as github_project
from lib.mongo.connection import MongoConnection
from lib.runner.jenkins_srv import JenkinsSrv

from bson.objectid import ObjectId
from datetime import datetime
import re
import time
import json


def handle_build_history(request):
    repo_id = request.args.get("repo_id")
    if repo_id:
        project, err = github_project.get_single_project(repo_id)  
        if err:
            return json.dumps({"error": err})

    mongo = MongoConnection()

    # user = mongo.db.users.find_one({"email":"jml11@illinois.edu"})
    # prev_id = {"user":user["_id"]}
    # mongo.db.builds.delete_many(prev_id)

  

    builds = list(mongo.db.builds.find({"user": ObjectId(current_user.get_id())}).sort("created_at", direction=-1))

    def populate_build_item(build_entry):
        job = mongo.db.jobs.find_one({"_id": build_entry["job"]})
        return {
            "git_url": job["git_url"],
            "build_number": build_entry["build_number"],
            "build_time": build_entry["created_at"],
            "job_id": str(job["_id"]),
            "build_id": str(build_entry["_id"]),
            "build_status": build_entry["status"]
        }

    build_items = map(populate_build_item, builds)

    if repo_id: 
        build_items = filter(lambda b: project["name"].lower() in b["git_url"].lower(), build_items)

    build_items = list(build_items)

    return json.dumps({"build_items": build_items}), 200


def handle_build_get(request):
    build_id = request.args.get("build_id")

    mongo = MongoConnection()

    build_info = mongo.db.builds.find_one({"_id": ObjectId(build_id)})
    job_info = mongo.db.jobs.find_one({"_id": build_info["job"]})

    # if the build wasn't complete on last query, pull any updates from jenkins and save update
    if build_info["status"] != "SUCCESS" and build_info["status"] != "FAILURE":
        jsrv = JenkinsSrv()
        jsrv.connect_to_jenkins()

        try:
            jenk_build_info = jsrv.srv.get_build_info(str(build_info["job"]), build_info["build_number"])
            
            if jenk_build_info["result"] == None:
                jenk_build_info["result"] = "RUNNING"

            updated = False
            if build_info["status"] != jenk_build_info["result"]:
                build_info["status"] = jenk_build_info["result"]
                updated = True

            build_info["time_elapsed"] = time.time() * 1000 - jenk_build_info["timestamp"]

            if updated:
                mongo.db.builds.update_one(
                    {"_id": ObjectId(build_id)},
                    {"$set": {"status": build_info["status"], "time_elapsed": build_info["time_elapsed"]}}
                )
        except jenkins.JenkinsException:
            # jenkins hasn't created the build yet
            pass

    build_data = {
        "git_url": job_info["git_url"],
        "build_number": build_info["build_number"],
        "status": build_info["status"],
        "time_elapsed": build_info["time_elapsed"]
    }

    return json.dumps({"build_data": build_data}), 200


def handle_build_logs(request):
    build_id = request.args.get("build_id")

    mongo = MongoConnection()
    build_info = mongo.db.builds.find_one({"_id": ObjectId(build_id)})

    if build_info == None:
        return json.dumps({"error": "Invalid build id"}), 400

    job_id = str(build_info["job"])

    jsrv = JenkinsSrv()
    jsrv.connect_to_jenkins()

    logs = jsrv.get_build_logs(job_id, build_info["build_number"])
    log_lines = logs.split("\n")

    # NOTE: This is very important. This removes the top part of the logs, which expose
    # the credentials for the Azure file share.
    if "Beginning execution..." in log_lines:
        sec_safe_logs = log_lines[log_lines.index("Beginning execution..."):]
    else:
        sec_safe_logs = ["No logs available yet. Your build may still be starting up."]

    return json.dumps({"build_logs": sec_safe_logs}), 200
