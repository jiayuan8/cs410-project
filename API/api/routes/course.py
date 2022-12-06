from flask import Blueprint, request
from flask_login import login_required

from api.route_handler import course_route_handler

course_blueprint = Blueprint("course_blueprint", __name__)

@course_blueprint.route("/api/course", methods=["GET"])
@login_required
def course_get():
    return course_route_handler.course_get(request)

@course_blueprint.route("/api/course/create", methods=["POST"])
@login_required
def course_create():
    return course_route_handler.course_create(request)

@course_blueprint.route("/api/course/join", methods=["POST"])
@login_required
def course_join():
    return course_route_handler.course_join(request)

@course_blueprint.route("/api/course/list_all", methods=["GET"])
@login_required
def course_list_all():
    return course_route_handler.course_list_all(request)

@course_blueprint.route("/api/course/list_user", methods=["GET"])
@login_required
def course_list_user():
    return course_route_handler.course_list_user(request)

@course_blueprint.route("/api/course/list_owner", methods=["GET"])
@login_required
def course_list_owner():
    return course_route_handler.course_list_owner(request)