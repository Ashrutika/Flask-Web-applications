import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    MONGODB_SETTINGS = { 'db':'Broadcast' }
    #MONGO_URI = "mongodb://localhost:27017/new"