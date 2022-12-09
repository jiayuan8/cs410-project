from flask import Blueprint, request
from flask_login import login_required


file_submission_blueprint = Blueprint("file_submission_blueprint", __name__)

@file_submission_blueprint.route("/api/filesubmission/submit", methods=["POST"])
@login_required
def project_create():
    pass