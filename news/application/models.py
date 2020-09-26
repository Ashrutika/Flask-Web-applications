from application import app
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id = db.IntField(unique=True)
    name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    user_type = db.StringField()
    password = db.StringField()

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password,password)

class News(db.Document):
    news_id = db.IntField(unique=True)
    author_name = db.StringField()
    date = db.DateField()
    title = db.StringField()
    headline = db.StringField()
    description = db.StringField()
   

