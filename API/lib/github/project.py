from flask_login import current_user

from app import redis_client

import base64
import json
import requests

def create_project(project_name, project_short_description, project_readme, project_zip):
    github_config = json.loads(open("github_config.json").read())

    projecthost_api_base = github_config["projecthost_api_base"]
    projecthost_api_username = github_config["projecthost_api_username"]
    projecthost_org_id = github_config["projecthost_org_id"]
    projecthost_api_key = github_config["projecthost_api_key"]

    repo_data_key = f"/orgs/{projecthost_org_id}/repos"
    full_request_url = f"https://{projecthost_api_username}:{projecthost_api_key}@" + projecthost_api_base + repo_data_key

    # create repo
    payload = {
        "name": project_name,
        "description": project_short_description
    }
    resp = requests.post(full_request_url, data=json.dumps(payload))
    if resp.status_code != 201:
        return None, resp.text
    repo_data = resp.json()
    repo_id = repo_data["id"]
    html_url = repo_data["html_url"]
    print("repo id",repo_id,flush=True)
    project_data = {
        "repo_id": repo_id,
        "repo_url": html_url
    }

    # push readme
    full_request_url = f"https://{projecthost_api_username}:{projecthost_api_key}@" + projecthost_api_base + f"/repos/{projecthost_org_id}/{project_name}/contents/README.md"
    payload = {
        "message": "push README.md",
        "content": base64.b64encode(project_readme.read()).decode("utf-8")
    }
    resp = requests.put(full_request_url, data=json.dumps(payload))
    if resp.status_code != 201:
        return repo_id, resp.text

    # push zip
    full_request_url = f"https://{projecthost_api_username}:{projecthost_api_key}@" + projecthost_api_base + f"/repos/{projecthost_org_id}/{project_name}/contents/{project_zip.name}.zip"
    payload = {
        "message": f"push {project_zip.name}",
        "content": base64.b64encode(project_zip.read()).decode("utf-8")
    }
    resp = requests.put(full_request_url, data=json.dumps(payload))
    if resp.status_code != 201:
        return repo_id, resp.text

    # empty github cache so new project shows
    redis_client.delete(repo_data_key)

    return project_data, None


def get_all_projects():
    github_config = json.loads(open("github_config.json").read())

    projecthost_api_base = github_config["projecthost_api_base"]
    projecthost_api_username = github_config["projecthost_api_username"]
    projecthost_org_id = github_config["projecthost_org_id"]
    projecthost_api_key = github_config["projecthost_api_key"]

    repo_data_key = f"/orgs/{projecthost_org_id}/repos"

    try:
        return json.loads(redis_client[repo_data_key])
    except Exception as e:
        print(e)
        full_request_url = f"https://{projecthost_api_username}:{projecthost_api_key}@" + projecthost_api_base + f"/orgs/{projecthost_org_id}/repos"
        resp = requests.get(full_request_url)
        response_data = resp.json()

        redis_client.set(repo_data_key, json.dumps(response_data), 30) # 30 seconds

        return response_data


def get_single_project(project_repo_id):
    try:
        project_repo_id = int(project_repo_id)
    except:
        return None, "Error: provided project_repo_id is not an int."

    github_config = json.loads(open("github_config.json").read())
    projecthost_org_id = github_config["projecthost_org_id"]
    repo_data_key = f"/orgs/{projecthost_org_id}/repos"

    try:
        all_project_data = json.loads(redis_client[repo_data_key])
    except Exception as e:
        print(e)
        all_project_data = get_all_projects()

    filtered_project_data = list(filter(lambda p: p["id"] == project_repo_id, all_project_data))
    if len(filtered_project_data) == 0:
        return None, "Error: requested project does not exist."

    if len(filtered_project_data) > 1:
        return None, "Error: project id matched more than one project. THIS SHOULD NEVER HAPPEN."

    # there should only be one matching entry with this project id
    return filtered_project_data[0], None


def is_forked_by_accounts(external_accounts, project):
    github_config = json.loads(open("github_config.json").read())

    projecthost_api_base = github_config["projecthost_api_base"]
    projecthost_api_username = github_config["projecthost_api_username"]
    projecthost_org_id = github_config["projecthost_org_id"]
    projecthost_api_key = github_config["projecthost_api_key"]

    repo = project["name"]
    owner = project["owner"]["login"]

    auth_url = f"https://{projecthost_api_username}:{projecthost_api_key}@" + projecthost_api_base
    api_url = f"/repos/{owner}/{repo}/forks"

    github_usernames = set(map(lambda acc: acc["username"], external_accounts))

    user_id = current_user.get_id()
    fork_data_key = api_url + "_" + user_id
    try:
        return redis_client[fork_data_key] == b'1'
    except:
        pass

    full_request_url = auth_url + api_url

    resp = requests.get(full_request_url)
    fork_data = resp.json()

    for fork in fork_data:
        if fork["owner"]["login"] in github_usernames:
            redis_client.set(fork_data_key, 1, 30) # 30 seconds
            return True

    redis_client.set(fork_data_key, 0, 30) # 30 seconds
    return False