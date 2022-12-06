from flask import Blueprint, request
from flask_login import login_required

from api.route_handler import external_account_route_handler

external_account_blueprint = Blueprint("external_account_blueprint", __name__)

@external_account_blueprint.route("/api/externalaccount/link", methods=["POST"])
@login_required
def link():
    return external_account_route_handler.handle_link(request)

@external_account_blueprint.route("/api/externalaccount/all", methods=["GET"])
@login_required
def get_all():
    return external_account_route_handler.handle_get_all(request)

@external_account_blueprint.route("/api/externalaccount/deleteall", methods=["GET"])
@login_required
def delete_all():
    return external_account_route_handler.handle_delete_all(request)