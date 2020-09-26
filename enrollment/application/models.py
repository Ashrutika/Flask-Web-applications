import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_pymongo import PyMongo

#mongo = PyMongo(app)

'''class Clients(mongo.db.Document):
    name = mongo.db.StringField(max_length=50)
    user_id = mongo.db.IntField(unique=True)'''

class User(db.Document):
    user_id = db.IntField(unique=True)
    name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField()

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password,password)

class Courses(db.Document):
    course_id = db.StringField(max_length=10,unique=True)
    title = db.StringField(max_length=50)
    description = db.StringField(max_length=200)
    credits = db.IntField()
    term = db.StringField(max_length=50)

class Enroll(db.Document):
     user_id = db.IntField()
     courseId = db.StringField(max_length=10)

