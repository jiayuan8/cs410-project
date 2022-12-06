from flask import Blueprint, request
from flask_login import login_required

from api.route_handler import project_route_handler

project_blueprint = Blueprint("project_blueprint", __name__)

@project_blueprint.route("/api/project/list_all", methods=["GET"])
@login_required
def project_list_all():
    return project_route_handler.list_all(request)
    
@project_blueprint.route("/api/project/list_user", methods=["GET"])
@login_required
def project_list_user():
    return project_route_handler.list_user(request)

@project_blueprint.route("/api/project/list_owner", methods=["GET"])
@login_required
def project_list_owner():
    return project_route_handler.list_owner(request)

@project_blueprint.route("/api/project/list_course", methods=["GET"])
@login_required
def project_list_course():
    return project_route_handler.list_course(request)

@project_blueprint.route("/api/project/create", methods=["POST"])
@login_required
def project_create():
    return project_route_handler.project_create(request)

@project_blueprint.route("/api/project", methods=["GET"])
@login_required
def project_get():
    return project_route_handler.project_get(request)

@project_blueprint.route("/api/project/leaderboard/new", methods=["POST"])
@login_required
def project_leaderboard_create():
    return project_route_handler.project_leaderboard_create(request)

@project_blueprint.route("/api/project/leaderboard", methods=["GET"])
@login_required
def project_leaderboard_get():
    return project_route_handler.project_leaderboard_get(request)

@project_blueprint.route("/api/project/leaderboard/ownership", methods=["GET"])
@login_required
def project_leaderboard_ownership_get():
    return project_route_handler.project_leaderboard_ownership_get(request)

@project_blueprint.route("/api/project/leaderboard/export", methods=["GET"])
@login_required
def project_leaderboard_export():
    return project_route_handler.project_leaderboard_export(request)

@project_blueprint.route("/api/project/leaderboard/submit", methods=["POST"])
def project_leaderboard_submit():
    return project_route_handler.project_leaderboard_submit(request)