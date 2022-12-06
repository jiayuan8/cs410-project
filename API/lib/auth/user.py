from flask_login import current_user

class User:
    def __init__(self, mongo_user_obj):
        self.id = mongo_user_obj["_id"]
        self.email = mongo_user_obj["email"]
        
    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

def get_user_id():
    """General get_user_id, allows for stubbing user loads in tests"""
    return current_user.get_id()
