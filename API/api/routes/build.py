from flask import Blueprint, request
from flask_login import login_required

from api.route_handler import build_route_handler

build_blueprint = Blueprint("build_blueprint", __name__)

@build_blueprint.route("/api/build", methods=["GET"])
@login_required
def build_get():
    request.ROUTE_PATH = "/api/build"
    return build_route_handler.handle_build_get(request)

@build_blueprint.route("/api/build/history", methods=["GET"])
@login_required
def build_history():
    request.ROUTE_PATH = "/api/build/history"
    return build_route_handler.handle_build_history(request)

@build_blueprint.route("/api/build/logs", methods=["GET"])
@login_required
def build_logs():
    request.ROUTE_PATH = "/api/build/logs"
    return build_route_handler.handle_build_logs(request)