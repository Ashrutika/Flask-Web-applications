import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xa6\x15\xc8\x946\xfe\x82\xb7\xcdu}R\xf1-h)'

    MONGODB_SETTINGS = { 'db':'Enrollment' }
    #MONGO_URI = "mongodb://localhost:27017/Enrollment"