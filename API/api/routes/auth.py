from flask import Blueprint, request

from api.route_handler import auth_route_handler

auth_blueprint = Blueprint("auth_blueprint", __name__)

@auth_blueprint.route("/api/login", methods=["POST"])
def login():
    return auth_route_handler.login_handler(request)

@auth_blueprint.route("/api/signup", methods=["POST"])
def signup():
    return auth_route_handler.signup_handler(request)

@auth_blueprint.route("/api/logout", methods=["GET"])
def logout():
    return auth_route_handler.logout_handler()

@auth_blueprint.route("/api/login_status", methods=["GET"])
def login_status():
    return auth_route_handler.login_status_handler()