from schema import db

class Lti(db.DynamicDocument):
    user = db.StringField(required=True)
    submission_id = db.StringField(required=True)
   