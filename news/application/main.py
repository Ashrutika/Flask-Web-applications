from application import app, db
from flask import render_template, request, url_for, json, jsonify, Response, redirect, session, flash
from application.models import User, News
from application.forms import LoginForm, RegisterForm, AddNews
from datetime import datetime
#from flask_restplus import Resource

@app.route('/')
def home():
	return render_template('home.html',home=True)

@app.route('/news',methods = ['POST','GET'])
def news():
	all_news = News.objects.all()
	return render_template('news.html',all_news=all_news,title="All News",news=True)

@app.route('/register',methods = ['POST','GET'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
    		
		user_id = User.objects.count() + 1
		name = form.name.data
		email = form.email.data
		user_type = form.language.data
		password = form.password.data
		
		user = User(user_id=user_id,name=name,email=email,user_type=user_type)
		user.set_password(password)
		user.save()
		flash("{} you are successfully registered :) ".format(name),"success")
		return redirect(url_for('login'))
	return render_template('register.html',title="Registration",form=form,register=True)

@app.route('/login',methods = ['POST','GET'])
def login():
	if session.get('name'):
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		user = User.objects(email=email).first()
		if user and user.get_password(password):
			session['user_id'] = user.user_id
			session['name'] = user.name
			session['type'] = user.user_type
			flash("{} you are successfully logged in :) ".format(user.name),"success")
			return redirect(url_for('home'))
		else:
			flash("You are not registered ! please register :)","danger")
			return redirect(url_for('register'))

	return render_template('login.html',form=form,title="Login",login=True)

@app.route('/logout')
def logout():
	session.pop('name',None)
	session.pop('type',None) 
	session.pop('user_id',None)
	flash('You are logged out',"success")
	return redirect(url_for('home'))

@app.route('/addnews',methods = ['POST','GET'])
def addnews():
	form = AddNews()
	if form.validate_on_submit():
		news_id = News.objects.count() + 1
		title = form.title.data
		headline = form.headline.data
		name = session.get('name')
		description = form.description.data
		News(news_id=news_id,title=title,description=description,author_name=name,headline=headline,date=datetime.now()).save()
		flash("{} News successfully added :) ".format(title),"success")
		return redirect(url_for('news'))
	return render_template("addnews.html",addnews=True,form=form,title="Add News")


@app.route('/mynews',methods = ['POST','GET'])
def mynews():
	name = session.get('name')
	all_news = list(User.objects.aggregate(*[
	{
	'$lookup': {
	'from': 'news', 
	'localField': 'name', 
	'foreignField': 'author_name', 
	'as': 'e1'
        }
	}, {
	'$unwind': {
	'path': '$e1', 
	'includeArrayIndex': 'e1_id', 
	'preserveNullAndEmptyArrays': False
	}
	}, {
	'$match': {
	'name': name
	}
	}
	]))
	return render_template("mynews.html",mynews=True,data=all_news,title="My News")
		
@app.route('/contact')
def contact():
	return render_template('contact.html',contact=True)
