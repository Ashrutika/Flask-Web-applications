from flask import Flask, redirect, url_for, request, flash, abort, session, jsonify, Blueprint
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


@app.route('/')
def home():
	return render_template('home.html')

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	location =  db.Column(db.String(50))
	date_created = db.Column(db.DateTime, default=datetime.now)


@app.route('/data',methods = ['POST','GET'])
def index():
	if request.method == 'POST':
		name = request.form['name']
		loc = request.form['loc']
		user = User(name=name, location=loc)
		db.session.add(user)
		db.session.commit()
	
		return render_template('display.html',name=request.form['name'],location=request.form['loc'])
	else:
		return redirect(url_for('home'))

'''@app.route('/<name>')
def get_user(name):
	
	
	return  render_template('display.html',name=user.name,location=user.location)'''
	

