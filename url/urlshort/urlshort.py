from flask import redirect, url_for, request, flash, abort, session, jsonify, Blueprint
from flask import render_template
import os
import json
from werkzeug.utils  import secure_filename

bp = Blueprint('urlshort',__name__)
#APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#print("path",APP_ROOT)

@bp.route('/')
def home():
	return render_template("home.html" , codes=session.keys())


@bp.route('/url-page', methods = ['POST','GET'])
def url_page():
	if request.method == 'POST':
		urls = {}
		#url = []
		if os.path.exists('url.json'):
			with open('url.json') as urls_file:
				urls = json.load(urls_file)
			
		if request.form['code'] in urls.keys():
			flash("This short code already been taken please specify other")
			return redirect(url_for('urlshort.home'))

		if 'url' in request.form.keys():
			urls[request.form['code']] = {"url":request.form['url']}
		else:
			f = request.files['file']
			fullname = request.form['code'] + secure_filename(f.filename)
			f.save("/home/root1/flask/url/urlshort/static/files/" + fullname)
			urls[request.form['code']] = {"file": fullname}
				
		with open('url.json','w') as url_file:
			json.dump(urls,url_file)
			session[request.form['code']] = True
    		
		return render_template("url.html",code=request.form['code'])
	else:
		return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_url(code):
	if os.path.exists('url.json'):
		with open('url.json') as urls_file:
			urls = json.load(urls_file)
			if code in urls.keys():
				if 'url' in urls[code].keys():
					return redirect(urls[code]['url'])
				else:
					return redirect(url_for('static',filename='files/' + urls[code]['file']))
	return abort(404)

@bp.errorhandler(404)
def page_not(error):
	return render_template('page-not.html'), 404

@bp.route('/api')
def session_api():
	return jsonify(list(session.keys()))

