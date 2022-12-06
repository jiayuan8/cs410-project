from flask import Blueprint, request

from api.route_handler import lti_route_handler

lti_blueprint = Blueprint("lti_blueprint", __name__)

@lti_blueprint.route("/api/lti_auth/", methods=["POST"])
def login():
    return lti_route_handler.auth_handler(request)