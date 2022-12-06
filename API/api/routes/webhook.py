from flask import Blueprint, request

from api.route_handler import webhook_route_handler

webhook_blueprint = Blueprint("webhook_blueprint", __name__)

@webhook_blueprint.route("/api/webhook/trigger", methods=["POST"])
def trigger_from_webhook():
    return webhook_route_handler.webhook_trigger(request)
    