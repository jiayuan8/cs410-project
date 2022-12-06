from flask import Blueprint, request, render_template

index_blueprint = Blueprint("index_blueprint", __name__)

@index_blueprint.route('/', methods=["GET"], defaults={'path': ''})
@index_blueprint.route('/<path:path>')
def index(path):
    return render_template("index.html")