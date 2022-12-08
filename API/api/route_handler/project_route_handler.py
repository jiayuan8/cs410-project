from flask_login import current_user
from werkzeug.utils import secure_filename
from lib.config import loader
import lib.github.project as github_project
from lib.mongo.connection import MongoConnection
from lib.teacher import teacher
import os
from bson.objectid import ObjectId
import csv
import json
import random
import string
import oauth2 as oauth
from itertools import groupby

def project_create(request):
    project_readme = request.files["project_readme"]
    project_zip = request.files["project_zipfile"]
    project_name = request.form["projectName"]
    project_short_description = request.form["projectShortDescription"]
    project_course_name = None if request.form["projectCourse"] == "null" else request.form["projectCourse"]
    auto_recommend_materials = True if request.form["autoRecommendMaterials"] == "true" else False
    required_files = json.loads(request.form["requiredFiles"])
    has_required_files = True if len(required_files) > 0 else False

    print(has_required_files, required_files)

    if len(project_name.split(" ")) > 1:
        return json.dumps({"error": "Spaces are not allowed in the project name."}), 400

    zip_filename = secure_filename(project_zip.filename)
    if len(zip_filename) < 5 or zip_filename[-4:].lower() != ".zip":
        return json.dumps({
            "error": f"Only .zip files can be accepted for project contents. Please make sure your file has a .zip extension."
        }), 400

    readme_filename = secure_filename(project_readme.filename)
    if len(readme_filename) < 4 or readme_filename[-3:].lower() != ".md":
        return json.dumps({
            "error": f"Only .md files can be accepted for project readme. Please make sure your file has a .md extension."
        }), 400

    project_data, err = github_project.create_project(project_name, project_short_description, project_readme, project_zip)
    if err:
        return json.dumps({"error": err}), 500

    # save repo_id and repo_url to mongo as project with owner
    mongo = MongoConnection()
    if project_course_name:
        project_course = mongo.db.courses.find_one({"name": project_course_name, "owner": ObjectId(current_user.get_id())})
        project_course_id = project_course["_id"]
    else:
        project_course_id = None

    project_id = mongo.db.projects.insert_one({
        "owner": ObjectId(current_user.get_id()),
        "repo_id": project_data["repo_id"],
        "repo_url": project_data["repo_url"],
        "name": project_name,
        "course": project_course_id,
        "auto_recommend_materials": auto_recommend_materials,
        "has_required_files": has_required_files,
        "required_files": required_files
    }).inserted_id

    if auto_recommend_materials:
        coursera_materials = teacher.recommend_materials(open(readme_filename).read())
        for mat in coursera_materials:
            mongo.db.project_materials.insert_one({
                "project_id": project_id,
                "course_link": mat["course_link"],
                "lesson_name": mat["lesson_name"]
            })

    return json.dumps({"project_url": f"/project/view/{project_data['repo_id']}"}), 200


def list_all(request):
    all_projects = github_project.get_all_projects()
    formatted_projects = list(map(_format_project, all_projects))
    return json.dumps({"projects": formatted_projects}), 200


def list_user(request):
    mongo = MongoConnection()
    external_accounts = list(mongo.db.external_accounts.find({"user": ObjectId(current_user.get_id())}))

    all_projects = github_project.get_all_projects()

    def is_forked_by_current_user(project):
        return github_project.is_forked_by_accounts(external_accounts, project)

    users_projects = filter(is_forked_by_current_user, all_projects)
    formatted_projects = list(map(_format_project, users_projects))

    return json.dumps({"projects": formatted_projects}), 200


def list_owner(request):
    mongo = MongoConnection()
    projects = list(mongo.db.projects.find({"owner": ObjectId(current_user.get_id())}))
    repo_ids = set([p["repo_id"] for p in projects])

    all_projects = github_project.get_all_projects()

    def is_owned_by_current_user(project):
        return project["id"] in repo_ids

    owned_projects = filter(is_owned_by_current_user, all_projects)
    formatted_projects = list(map(_format_project, owned_projects))
    return json.dumps({"projects": formatted_projects}), 200


def list_course(request):
    course_id = request.args.get("course_id")
    mongo = MongoConnection()
    course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        return json.dumps({"error": "Requested course does not exist."}), 400

    enrollment = mongo.db.course_enrollments.find_one({"user": ObjectId(current_user.get_id())})

    if not (course["owner"] == ObjectId(current_user.get_id()) or enrollment or course["public"]):
        return json.dumps({"error": "Not authorized to retrieve projects for this course."}), 401

    all_projects = github_project.get_all_projects()
    project_metadata = list(mongo.db.projects.find({"course": ObjectId(course_id)}))
    project_repo_ids = set([p["repo_id"] for p in project_metadata])
    projects = filter(lambda p: p["id"] in project_repo_ids, all_projects)
    formatted_projects = list(map(_format_project, projects))
    return json.dumps({"projects": formatted_projects}), 200


def project_get(request):
    project_repo_id = request.args.get("project_repo_id")

    project_github_data, err = github_project.get_single_project(project_repo_id)
    if err:
        return json.dumps({"error": err}), 400

    formatted_project = _format_project(project_github_data)
    return json.dumps({"project": formatted_project}), 200


def project_leaderboard_create(request):
    leaderboard_data = json.loads(request.data)
    project_name = leaderboard_data["project"]
    leaderboard_columns = leaderboard_data["columns"]
    rank_column = leaderboard_data["rankingColumn"]
    hide_results = leaderboard_data["hideResults"]

    mongo = MongoConnection()
    project = mongo.db.projects.find_one({"name": project_name})
    if not project:
        return json.dumps({"error": "Specified project does not exist"}), 400 # this should not happen

    leaderboard = mongo.db.leaderboards.find_one({"project_repo_id": project["repo_id"]})
    if leaderboard:
        return json.dumps({"error": "Specified project already has a leaderboard"}), 400 # this should not happen

    new_leaderboard = mongo.db.leaderboards.insert_one({
        "project_repo_id": project["repo_id"],
        "columns": leaderboard_columns,
        "rank_column": rank_column,
        "hide_results": hide_results
    })

    if not new_leaderboard:
        return json.dumps({"error": "Failed to create new leaderboard"}), 500

    leaderboard_payload = {"leaderboard_url": f"/project/leaderboard/{project['repo_id']}"}
    return json.dumps(leaderboard_payload), 200

def get_username(name):
    if name =="Bhavya":
        name = "baseline"
    return name 


def project_leaderboard_get(request):
    project_repo_id = request.args.get("project_repo_id")

    try:
        project_repo_id = int(project_repo_id)
    except:
        return json.dumps({"error": "Provided project repo id is not an int"}), 400

    mongo = MongoConnection()
    leaderboard = mongo.db.leaderboards.find_one({"project_repo_id": project_repo_id})
    if not leaderboard:
        return json.dumps({"error": "Specified project does not have a leaderboard"}), 400

    all_leaderboard_results = list(mongo.db.leaderboard_results.find({"leaderboard_id": leaderboard["_id"]}))
    project = mongo.db.projects.find_one({"repo_id": project_repo_id})
    # print(leaderboard["_id"],project_repo_id,all_leaderboard_results,flush=True)

    if leaderboard["hide_results"] and project["owner"] != ObjectId(current_user.get_id()):
        all_leaderboard_results = list(
            filter(lambda res: res["user_id"] == ObjectId(current_user.get_id()), all_leaderboard_results)
        )
    all_leaderboard_results = sorted(all_leaderboard_results, key=lambda x:x['username'])

    all_latest_res = []
    # print(all_leaderboard_results,flush=True)

    for k,v in groupby(all_leaderboard_results,key=lambda x:str(x['username'])):
        latest_res = max(list(v), key=lambda x:int(x['submission_number']))
        all_latest_res.append(latest_res)

    # print(all_latest_res,flush=True)

    leaderboard_res = [(res_obj["results"], get_username(res_obj["username"]), res_obj["submission_number"]) for res_obj in all_latest_res]

    leaderboard_res = sorted(leaderboard_res, key=lambda row: row[0][leaderboard["columns"].index(leaderboard["rank_column"])], reverse=True)
    ranked_results = [{"rank": i + 1, "username": leaderboard_res[i][1], "submission_number": leaderboard_res[i][2], "data": leaderboard_res[i][0]} for i in range(len(leaderboard_res))]
    
    leaderboard_data = {
        "columns": leaderboard["columns"],
        "rows": ranked_results,
        "leaderboard_id": str(leaderboard["_id"])
    }

    return json.dumps(leaderboard_data), 200  



def upload_grade_to_coursera(grade,submission_id):
    with open('lti_config.json','r') as f:
        lti_config = json.loads(f.read())
    print(submission_id,grade,flush=True)

    xml = f"""<?xml version = "1.0" encoding = "UTF-8"?>
    <imsx_POXEnvelopeRequest xmlns = "http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">
      <imsx_POXHeader>
        <imsx_POXRequestHeaderInfo>
          <imsx_version>V1.0</imsx_version>
        </imsx_POXRequestHeaderInfo>
      </imsx_POXHeader>
      <imsx_POXBody>
        <replaceResultRequest>
          <resultRecord>
            <sourcedGUID>
              <sourcedId>{submission_id}</sourcedId>
            </sourcedGUID>
            <result>
              <resultScore>
                <language>en</language>
                <textString>{grade}</textString>
              </resultScore>
            </result>
          </resultRecord>
        </replaceResultRequest>
      </imsx_POXBody>
    </imsx_POXEnvelopeRequest>""".encode('utf-8')


    print(xml,flush=True)
    url = 'https://api.coursera.org/api/onDemandLtiOutcomes.v1'
    headers = {'Content-Type': 'application/xml',}
    con = oauth.Consumer(key=lti_config['coursera_consumer_key'], secret=lti_config['coursera_secret'])
    client = oauth.Client(con)
    resp, content = client.request(url, "POST",body=xml,headers=headers)
    
    print(resp,content,flush=True)



def project_leaderboard_submit(request):
    
    leaderboard_id = request.args.get("leaderboard")
    if not leaderboard_id:
        return json.dumps({"error": "No leaderboard specified"}), 400

    mongo = MongoConnection()
    if not mongo.db.leaderboards.find_one({"_id": ObjectId(leaderboard_id)}):
        return json.dumps({"error": "Specified leaderboard does not exist"}), 400

    submission_data = json.loads(request.data)

    if "email" not in submission_data:
        return json.dumps({"error": "required field 'email' missing in request body"}), 400

    if "results" not in submission_data:
        return json.dumps({"error": "required field 'results' missing in request body"}), 400

    email = submission_data["email"].lower().strip()

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return json.dumps({"error": "Invalid user email"}), 400

    previous_submissions = list(mongo.db.leaderboard_results.find({
        "leaderboard_id": ObjectId(leaderboard_id),
        "user_id": user["_id"]
    }))
    submission_number = len(previous_submissions) + 1


    mongo.db.leaderboard_results.insert_one({
        "submission_number": submission_number,
        "leaderboard_id": ObjectId(leaderboard_id),
         "user_id": user["_id"],
        "results": submission_data["results"],
        "username": user["username"]
    })
    coursera_submission = mongo.db.coursera_submissions.find_one({"user": email, "leaderboard_id": leaderboard_id})
    if coursera_submission is not None:
        upload_grade_to_coursera(float(submission_data["results"][-1]),coursera_submission["submission_id"]) #last column reserved for coursera grade


    return json.dumps({}), 200


def project_leaderboard_ownership_get(request):
    project_repo_id = request.args.get("project_repo_id")

    try:
        project_repo_id = int(project_repo_id)
    except:
        return json.dumps({"error": "Specified project repo id is not an int"}), 400

    mongo = MongoConnection()
    project = mongo.db.projects.find_one({"repo_id": project_repo_id})
    if not project:
        return json.dumps({"error": "Specified project does not exist"}), 400

    if project["owner"] == ObjectId(current_user.get_id()):
        is_owner = True
    else:
        is_owner = False

    return json.dumps({"is_owner": is_owner}), 200


def project_leaderboard_export(request):
    project_repo_id = request.args.get("project_repo_id")

    try:
        project_repo_id = int(project_repo_id)
    except:
        return json.dumps({"error": "Specified project repo id is not an int"}), 400

    mongo = MongoConnection()
    project = mongo.db.projects.find_one({"repo_id": project_repo_id})
    if not project:
        return json.dumps({"error": "Specified project does not exist"}), 400

    if project["owner"] != ObjectId(current_user.get_id()):
        return json.dumps({"error": "User not authorized for this action"}), 401

    leaderboard = mongo.db.leaderboards.find_one({"project_repo_id": project_repo_id})
    all_leaderboard_results = mongo.db.leaderboard_results.find({"leaderboard_id": leaderboard["_id"]})

    filename = "static/exports/" + ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + "_export.csv"
    localpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),filename)
    with open(localpath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        col_names = ["submission_number", "user_id","email"] + leaderboard["columns"]
        writer.writerow(col_names)
        for leaderboard_result in all_leaderboard_results:
            try:
                email = mongo.db.users.find_one({"_id":leaderboard_result["user_id"]})["email"]
            except:
                email = 'deleted'
            row = [
                leaderboard_result["submission_number"],
                leaderboard_result["user_id"],
                email,
            ] + leaderboard_result["results"]
            writer.writerow(row)
        csvfile.close()
        
    api_domain = loader.load_server_config()["host_domain"]
    return json.dumps({"download_url": f"{api_domain}/{filename}"}), 200


def _format_project(project):
    mongo = MongoConnection()
    project_metadata = mongo.db.projects.find_one({"repo_id": project["id"]})

    additional_fields = {}
    if project_metadata:
        additional_fields = {
            "has_metadata_fields": True,
            "is_owner": project_metadata["owner"] == ObjectId(current_user.get_id())
        }

        leaderboard = mongo.db.leaderboards.find_one({"project_repo_id": project["id"]})
        if leaderboard:
            additional_fields["has_leaderboard"] = True
            additional_fields["leaderboard_url"] = f"/project/leaderboard/{project['id']}"

        if project_metadata["auto_recommend_materials"]:
            materials = list(mongo.db.project_materials.find({"project_id": project_metadata["_id"]}))
            grouped_materials = {}
            links = []
            for mat in materials:
                if mat["course_link"] in grouped_materials:
                    grouped_materials[mat["course_link"]].append(mat["lesson_name"])
                else:
                    grouped_materials[mat["course_link"]] = [mat["lesson_name"]]
                    links.append(mat["course_link"])

            additional_fields["has_recommended_materials"] = True
            additional_fields["recommended_materials"] = grouped_materials
            additional_fields["recommended_materials_links"] = links

        if project_metadata["has_required_files"]:
            additional_fields["has_required_files"] = True
            additional_fields["required_files"] = project_metadata["required_files"]
        else:
            additional_fields["has_required_files"] = False

    ## ** merges the dicts and the second dict overrides the first
    return {**{
        "repo_id": project["id"],
        "title": project["name"],
        "num_learners": project["forks_count"],
        "short_description": project["description"],
        "hosting_url": project["html_url"],
        "project_view_url": f"/project/view/{project['id']}",
        "has_metadata_fields": False, # overrides if has metadata fields
        "has_leaderboard": False # overrides with metadata fields
    }, **additional_fields}