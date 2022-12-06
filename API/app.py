from flask import Flask
from flask_login import LoginManager
import redis

from lib.auth.user import User
from lib.config import loader
from lib.mongo.connection import MongoConnection

from bson.objectid import ObjectId
import json

server_config = loader.load_server_config()

app = Flask(__name__)
app.secret_key = server_config["secret_key"]

# create redis client
redis_config = loader.load_redis_config()
redis_client = redis.Redis(host=redis_config["host"], port=6379)

# setup login manager for session tracking
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    mongo = MongoConnection()
    m_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    user = User(m_user)
    return user