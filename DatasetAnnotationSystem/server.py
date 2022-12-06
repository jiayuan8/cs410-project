from flask import Flask, jsonify, flash, request
from flask_restful import Api
from schema import db
from schema.User import User
from schema.Assignment import Assignment
from schema.Query import Query
from schema.Document import Document
from schema.Dataset import Dataset
from schema.Annotation import Annotation
from schema.Class import Class

from schema.Lti import Lti
from api.indexAPI import IndexAPI
from api.searchAPI import SearchAPI
from api.annotationAPI import AnnotationAPI
from api.uploadAPI import UploadAPI
from api.assignmentAPI import AssignAPI, AssignmentAPI, AssignmentUpdateAPI
from api.documentAPI import DocumentAPI
from api.documentAPI import DocumentsAPI
from api.datasetupdateAPI import DatasetUpdateAPI
from api.instructorAPI import InstructorAPI
from api.annotatorAPI import AnnotatorAPI
from api.queryAPI import QueryAPI
from api.querydeleteAPI import QueryDeleteAPI
from api.alertAPI import AlertAPI
from api.classAPI import ClassAPI
from api.extractAPI import ExtractAPI
from api.ltiAPI import LtiAPI
from flask_bcrypt import check_password_hash, generate_password_hash
import json
from util.exception import InvalidUsage

from flask import render_template, url_for, session, redirect, make_response, current_app
from authlib.flask.client import OAuth
import requests, os
import sys

app = Flask(__name__, static_folder='static/', static_url_path='')
app.config["SECRET_KEY"] = "secret"

# db settings only need to be specified in production
# defaults are used in development
env = os.environ["APP_ENV"]
if env == "prod":
    app.config['MONGODB_SETTINGS'] = {
       'db': 'prod',
       'host': 'mongo'
    }

cfg = json.loads(open('config.json').read())[env]
api = Api(app)

db.init_app(app)

api.add_resource(IndexAPI, '/')
api.add_resource(SearchAPI, '/search/<string:owner_id>/<string:ds_name>')
api.add_resource(AnnotationAPI, '/annotation')
api.add_resource(UploadAPI, '/upload')

api.add_resource(AssignAPI, '/assign')
api.add_resource(AssignmentAPI, '/assignment/<string:owner_id>/<string:assignment_name>')
api.add_resource(AssignmentUpdateAPI, '/assignment_update')

api.add_resource(QueryAPI, '/query')
api.add_resource(QueryDeleteAPI, '/query/delete')

api.add_resource(DocumentsAPI, '/documents')
api.add_resource(DocumentAPI, '/document')

api.add_resource(InstructorAPI, '/instructor')
api.add_resource(AnnotatorAPI, '/annotator')
api.add_resource(ClassAPI, '/class')

api.add_resource(DatasetUpdateAPI, '/dataset_update')

api.add_resource(AlertAPI, '/alert/<string:url>/<string:message>')
api.add_resource(ExtractAPI, '/extract')
api.add_resource(LtiAPI, '/lti_auth')

# Dataset.objects().delete()
# Annotation.objects().delete()
# Assignment.objects().delete()
# Document.objects().delete()
# Query.objects().delete()
# Class.objects().delete()
# User.objects(email='abs4@illinois.edu').delete()


# for ass in Assignment.objects():
#     print(ass.statuses)
#     for ann in ass.annotators:
#         print(ann)
#     sys.stdout.flush()
# for ann in Annotation.objects():

#     print(ann.annotator.name)
#     print(ann.query.content)
#     print(ann.judgement)
#     sys.stdout.flush()
# sys.stdout.flush()

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')


@app.route('/login',methods=['POST'])
def login():
    print(request.form)
    print(request.data)
    sys.stdout.flush()
    email = request.form.get("email").lower()
    password = request.form.get("password")
    m_user = User.objects(email=email).first()
    if not m_user or not check_password_hash(m_user["password"], password):
        flash('Invalid username or password')
        return redirect('/',code=303)
    else:
        session['user_id'] = str(m_user.id)

        return redirect('/')

@app.route('/signup',methods=['GET'])
def signup():
    return make_response(
            render_template("signup.html"), 200,
            {'Content-Type': 'text/html'})

@app.route('/signup/auth',methods=['POST'])
def signup_auth():
    params = request.form

    email = params["email"].lower()
    username = params["username"]
    password = params["password"]
    confirmed_password = params["confirmedPassword"]
    if email == '' or username == '' or password == '' or confirmed_password == '':
        flash('All fields must be filled')
        return redirect('/signup')

    if password != confirmed_password:
        flash('Passwords do not match.')
        return redirect('/signup')

    user = User.objects(email=email).first()
    if user:
        flash('An account already exists with this email address')
        return redirect('/signup')

    user = User.objects(name=username).first()
    if user:
        flash('An account already exists with this username')
        return redirect('/signup')

    pw_hash = generate_password_hash(password)
    sys.stdout.flush()
    new_user = User()
    new_user.name = username
    new_user.password = pw_hash
    new_user.email = email
    new_user.save()
    print("saved")
    sys.stdout.flush()
    flash('Account created successfully')

    return redirect('/')

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


if __name__ == '__main__':
    app.run(debug=True)
