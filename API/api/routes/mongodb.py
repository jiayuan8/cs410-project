from flask import Blueprint, request

from api.route_handler import mongodb_route_handler

mongodb_blueprint = Blueprint("mongodb_blueprint", __name__)

@mongodb_blueprint.route("/api/mongodb", methods=["POST"])
def entry():
	return {},200

@mongodb_blueprint.route("/api/mongodb/getrec", methods=["POST"])
def get_records():
    return mongodb_route_handler.get_records_handler(request)

@mongodb_blueprint.route("/api/mongodb/insert", methods=["POST"])
def insert_records():
    return mongodb_route_handler.insert_records_handler(request)

@mongodb_blueprint.route("/api/mongodb/delete", methods=["POST"])
def delete_records():
    return mongodb_route_handler.delete_records_handler(request)