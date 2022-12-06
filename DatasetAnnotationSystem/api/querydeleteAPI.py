from flask import make_response, render_template, current_app, jsonify, session
from flask_restful import Resource, reqparse

from schema.Query import Query
from schema.User import User

from bson.objectid import ObjectId

import json

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)

class QueryDeleteAPI(Resource):
    def post(self):
        args = parser.parse_args()

        query_id = args['query']

        user_id = session["user_id"]

        query = Query.objects(id=query_id).first()
        if query == None:
            return json.dumps({"error": "Specified query does not exist"}), 400

        if query.creator.id != ObjectId(user_id):
            return json.dumps({"error": "Unauthorized for this action"}), 401

        query.delete()

        return json.dumps({"message": "Successfully deleted query"}), 200
