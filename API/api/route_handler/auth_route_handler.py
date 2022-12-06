from flask import redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import check_password_hash, generate_password_hash

from lib.auth.user import User
from lib.mongo.connection import MongoConnection
import sys
import json

def login_handler(request):
    params = request.json

    email = params["email"].lower()
    password = params["password"]

    mongo = MongoConnection()


    m_user = mongo.db.users.find_one({"email": email})

    if not m_user or not check_password_hash(m_user["password"], password):
        return json.dumps({
            "error": "Invalid email or password."
        }), 400

    user = User(m_user)
    login_user(user, remember=True)

    return json.dumps({}), 200


def signup_handler(request):
    params = request.json

    email = params["email"].lower()
    username = params["username"]
    password = params["password"]
    confirmed_password = params["confirmedPassword"]

    if password != confirmed_password:
        return json.dumps({
            "error": "Passwords do not match."
        }), 400

    mongo = MongoConnection()

    user = mongo.db.users.find_one({"email": email})
    if user: 
        #hack to allow students to create a new account with same email in case they forgot their password, if they use some other email, need to manually delete any external 
        #linked account tied to github
        mongo.db.users.delete_many({"email":email})
        mongo.db.external_accounts.delete_many({"user":user["_id"]})
        mongo.db.jobs.delete_many({"user":user["_id"]})
        mongo.db.builds.delete_many({"user":user["_id"]})
        mongo.db.leaderboard_results.delete_many({"user_id":user["_id"]})
        mongo.db.course_enrollments.delete_many({"user":user["_id"]})
        mongo.db.coursera_submissions.delete_many({"user":email})
        # return json.dumps({
        #     "error": "An account already exists with this email address."
        # }), 400

    user = mongo.db.users.find_one({"username": username})
    if user:
        return json.dumps({
            "error": "An account already exists with this username."
        }), 400

    pw_hash = generate_password_hash(password)

    new_user_id = mongo.db.users.insert_one(
        {"email": email, "username": username, "password": pw_hash}
    ).inserted_id

    m_user = mongo.db.users.find_one({"_id": new_user_id})

    user = User(m_user)
    login_user(user, remember=True)

    return json.dumps({}), 200


def logout_handler():
    logout_user()
    return json.dumps({}), 200


def login_status_handler():
    return json.dumps({"authenticated": current_user.is_authenticated}), 200