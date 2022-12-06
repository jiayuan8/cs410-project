import os
import json

def load_server_config():
    env = os.environ["FLASK_ENV"]
    return json.loads(open("server_config.json").read())[env]

def load_redis_config():
    env = os.environ["FLASK_ENV"]
    return json.loads(open("redis_config.json").read())[env]