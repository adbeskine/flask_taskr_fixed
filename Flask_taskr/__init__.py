# Flask_taskr/__init__.py

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, url_for
import datetime

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



from Flask_taskr.users.views import users_blueprint
from Flask_taskr.tasks.views import tasks_blueprint
# from Flask_taskr.api.views import api
from Flask_taskr.api.views import api_bp

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_bp)


@app.errorhandler(404)
def not_found(error):
	if app.debug is not True:
		now = datetime.datetime.now()
		r = request.url
		with open('error.log', 'a') as f:
			current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
			f.write("\n404 error at {}: {}".format(current_timestamp, r))
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	if app.debug is not True:
		now = datetime.datetime.now()
		r = request.url
		with open('error.log', 'a') as f:
			current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
			f.write("\n500 error at {}: {}".format(current_timestamp, r))
	return render_template('500.html'), 500


	