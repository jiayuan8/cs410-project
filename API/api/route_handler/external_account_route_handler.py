from flask_login import current_user

from lib.mongo.connection import MongoConnection
from lib.runner.jenkins_srv import JenkinsSrv

from bson.objectid import ObjectId
import json

def handle_link(request):
    params = request.json
    
    username = params["username"].strip()
    host_domain = params["hostDomain"].strip()
    api_key = params["apiKey"].strip()

    mongo = MongoConnection()
    external_account_id = mongo.db.external_accounts.insert_one({
        "user": ObjectId(current_user.get_id()),
        "username": username,
        "host_domain": host_domain
    }).inserted_id

    print(username,external_account_id,flush=True)

    jsrv = JenkinsSrv()
    jsrv.connect_to_jenkins()
    create_success,txt = jsrv.create_credential_for_api_key(str(external_account_id), username, api_key)

    if create_success:
        return json.dumps({}), 200
    else:
        return json.dumps({"error": txt}), 500

def handle_get_all(request):
    mongo = MongoConnection()
    external_accounts = list(mongo.db.external_accounts.find({"user": ObjectId(current_user.get_id())}))
    
    def extract_account_info(account):
        return {
            "username": account["username"],
            "host_domain": account["host_domain"],
            "linked_date": account["_id"].generation_time.strftime("%m/%d/%Y")
        }

    formatted_accounts = list(map(extract_account_info, external_accounts))
    return json.dumps({"linked_accounts": formatted_accounts}), 200

def handle_delete_all(request):
    mongo = MongoConnection()
    del_user = { "user": ObjectId(current_user.get_id()) }
    mongo.db.external_accounts.delete_many(del_user)
    mongo.db.jobs.delete_many(del_user)
    mongo.db.builds.delete_many(del_user)
    return json.dumps({}), 200