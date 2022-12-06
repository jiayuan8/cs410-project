from api.routes.auth import auth_blueprint
from api.routes.build import build_blueprint
from api.routes.course import course_blueprint
from api.routes.external_account import external_account_blueprint
from api.routes.index import index_blueprint
from api.routes.project import project_blueprint
from api.routes.webhook import webhook_blueprint
from api.routes.lti import lti_blueprint
from api.routes.mongodb import mongodb_blueprint

from app import app

# register routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(build_blueprint)
app.register_blueprint(course_blueprint)
app.register_blueprint(external_account_blueprint)
app.register_blueprint(project_blueprint)
app.register_blueprint(webhook_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(lti_blueprint)
app.register_blueprint(mongodb_blueprint)

if __name__ == "__main__":
    app.run(debug=True)