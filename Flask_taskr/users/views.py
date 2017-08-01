# users.views

from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.exc import IntegrityError

from Flask_taskr.models import User
from .forms import RegisterForm, LoginForm
from Flask_taskr import db, bcrypt

################
#### config ####
################

users_blueprint = Blueprint('users', __name__)

##########################
#### helper functions ####
##########################

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('users.login'))
	return wrap

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')

################
#### routes ####
################

@users_blueprint.route('/logout/')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	flash('Goodbye!')
	return redirect(url_for('users.login'))

# @users_blueprint.route('/', methods = ['GET', 'POST'])
# def login():
	# error = None
	# form = LoginForm(request.form)
	# if request.method == 'POST':
		# if form.validate():	
			# user = User.query.filter_by(username = request.form['username']).first()
			# if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
				# session['logged_in'] = True
				# session['user_id'] = user.id
				# session['role'] = user.role
				# session['username'] = user.username
				# flash('Welcome!')
				# return redirect(url_for('tasks.tasks'))
			# else:
				# error = 'Invalid username or password.'
	# return render_template('login.html', form=form, error = error)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if request.method == 'POST':
		if form.validate():
			new_name = form.username.data
			password = form.password.data
			# new_user = User(form.username.data, form.password.data, form.email.data) for manually testing bad users and code  500
			new_user = User(form.username.data, bcrypt.generate_password_hash(form.password.data), form.email.data)
			try:
				db.session.add(new_user)
				db.session.commit()
				flash('New user registered. Welcome, {}, please log in'.format(new_name))
				return redirect(url_for('users.login'))				
			except IntegrityError:
				error = "That username and/or email already exist."
				return render_template('register.html', form=form, error=error)
		elif not form.validate():
			error = 'please fill in all fields correctly'
			return render_template('register.html', form=form, error=error)
	return render_template('register.html', form=RegisterForm())
