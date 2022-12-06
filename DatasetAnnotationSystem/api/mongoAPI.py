from flask import make_response, render_template, session, jsonify, redirect, current_app
from flask_restful import Resource, reqparse
from schema.Dataset import Dataset

from schema.User import User
from schema.Query import Query
from schema.Assignment import Assignment
import os, metapy

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('dataset', type=str)
parser.add_argument('query', type=str)
parser.add_argument('ranker', type=str)
parser.add_argument('params', type=dict)
parser.add_argument('deadline', type=str)
parser.add_argument('status', type=bool)
parser.add_argument('content', type=str)
parser.add_argument('creator', type=str)
parser.add_argument('doc_scores', type=dict)
parser.add_argument('num_results', type=int)



class MongoAPI(Resource):
    def post(self):
        args = parser.parse_args()
        owner = User.objects(id=owner_id).first()
        user_id = session['user_id']
        user = User.objects(id=user_id).first()

        assignment = Assignment.objects(name=assignment_name)  \
            .filter(owner=owner).first()

        # Allow re-submission
        #if assignment.statuses[str(user_id)]:
        #    return redirect("/annotator")
        for ann in Annotation.objects():

#     print(ann.annotator.name)
#     print(ann.query.content)
#     print(ann.judgement)
#     sys.stdout.flush()
# sys.stdout.flush()

        assignment.owner_name = assignment.owner.name
        assignment.ds_name = assignment.dataset.name
        assignment.ds_owner_id = str(assignment.dataset.owner.id)

        queries = Query.objects(assignment=assignment, creator=user, submitted=False)
        return make_response(
            render_template(
                "assignment.html",
                user = user,
                assignment = assignment,
                queries = queries
            ),
            200,headers)





