from application import app, db, api
from flask import render_template, request, url_for, json, jsonify, Response, redirect, session, flash
from application.models import User, Courses, Enroll
from application.forms import LoginForm, RegisterForm
from flask_restplus import Resource
from application.course_enrolled import course_list
#from flask_pymongo import PyMongo

#mongo = PyMongo(app)
#myuser = mongo.db.user
#course = mongo.db.courses
#enroll = mongo.db.enroll

########################################################

'''@api.route('/api','/api/')
class GetAndPost(Resource):
    #GET all
    def get(self):
        return jsonify(User.objects.all())
        
    #POST
    def post(self):
        data = api.payload

        user = User(user_id=data['user_id'],email=data['email'],name=data['name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    #GET one
    def get(self,idx):
        return jsonify(User.objects(user_id=idx))

    #PUT
    def put(self,idx):
        data = api.payload

        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    #DELETE
    def delete(self,idx):
        User.objects(user_id=idx).delete()
        return jsonify("User deleted")'''


########################################################

@app.route('/home')
def home():
    return render_template('home.html',home=True)

@app.route('/courses/')
@app.route('/courses/<term>')
def courses(term=None):
    #return render_template('courses.html',courseData=courseData,courses=True,term=term,logs=session.keys(),ans=session.values(),name=name)
    if term is None:
        term = "Spring 2020"

    all_courses = Courses.objects.order_by('course_id')
    return render_template('courses.html',allcourses=all_courses,courses=True,term=term)

@app.route('/login', methods = ['POST','GET'])
def login():
    print("in login")
    if session.get('name'):
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        print(User.objects.count())
        email = request.form["email"]
        password = request.form["password"]
        user = User.objects(email=email).first() 
        print(user)
        if user and user.get_password(password):
            flash("{} You are successfully logged in.".format(user.name),"success")
            print(True)
            session['user_id'] = user.user_id
            session['name'] = user.name
            return redirect(url_for('home'))
        else:
            flash("Sorry!! Try again","danger")
            print(False)
            return redirect(url_for('login'))
    return render_template('login.html', title="Login", form=form, login=True)

@app.route('/logout')
def logout():
    session['user_id'] = False
    session.pop('name',None)
    return redirect(url_for('home'))

@app.route('/register',methods = ['POST','GET'])
def register():
    if session.get('name'):
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        name = form.name.data
        
        user = User(user_id=user_id,email=email,name=name)
        user.set_password(password)
        user.save()
        flash("{} You are successfully registered.".format(name),"success")
        return redirect(url_for("home"))
    return render_template('register.html',title="Registration", form=form, register=True)

@app.route('/enroll', methods = ['POST','GET'])
def enroll():

        if not session.get('name'):
            return redirect(url_for('login'))

        courseId = request.form.get("id")
        course_title = request.form.get("title")
        user_id = session.get('user_id')
        print(courseId)
        if courseId:
            print(courseId)
            if Enroll.objects(user_id=user_id,courseId=courseId):
                #flash(course_title)
                flash("Course {} : Oops! You are already enrolled in this course".format(course_title),"danger")
                return redirect(url_for("courses"))
            else:
                Enroll(user_id=user_id,courseId=courseId).save()
                flash("You are successfully enrolled in {}".format(course_title),"success")
                #flash(course_title)
        
        courses = course_list(user_id) 
        return render_template('enroll.html',enroll=True,title="Enrollment",classes=courses)

'''@app.route('/api/')
@app.route('/api/<idx>')
def api(idx=None):
    if idx == None:
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    return Response(json.dumps(jdata),mimetype="application/json")'''


'''@app.route("/user")
def user():
    #Clients(name="shruti",user_id=1).save()
    #User(user_id=2,name="aditya").save()

    #users = myuser.find().sort("user_id",1)
    users = User.objects.order_by('user_id')
    x = []
    for item in users:
        x.append(item)
    return render_template("user.html",users=x)'''

'''class Register(db.Document):
    name = db.StringField(max_length=10)
    email = db.StringField(max_length=50,unique=True)
    password = db.StringField(max_length=10)

@app.route('/signup',methods = ['POST','GET'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    Register(name=name,email=email,password=password).save()
    return redirect(url_for('login'))

@app.route('/logging',methods = ['POST','GET'])
def logging():
    email = request.form['email']
    password = request.form['password']
    
    users = Register.objects.all()
    for user in users:
        if email == user.email and password == user.password:
            loggedin=True
            #session['loggedin'] = True
            session[request.form['email']] = True
            name=user.name
            break
        else:
            loggedin=False
            #session['loggedin'] = False
            session[request.form['email']] = False
            continue

    return redirect(url_for('courses',name=name))'''


