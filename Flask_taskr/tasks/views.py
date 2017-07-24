#tasks

from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.exc import IntegrityError

from .forms import AddTaskForm
from Flask_taskr import db
from Flask_taskr.models import Task

################
#### config ####
################

tasks_blueprint = Blueprint('tasks', __name__)

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

def open_tasks():
	if session['role'] == 'user':
		return db.session.query(Task).filter_by(status='1', user_id=session['user_id']).order_by(Task.due_date.asc())
	elif session['role'] == 'admin':
		return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())

def closed_tasks():
	if session['role'] == 'user':
		return db.session.query(Task).filter_by(status='0', user_id=session['user_id']).order_by(Task.due_date.asc())
	elif session['role'] == 'admin':
		return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

################
#### routes ####
################




@tasks_blueprint.route('/tasks/')
@login_required
def tasks():
	return render_template('tasks.html',
		form = AddTaskForm(request.form),
		open_tasks = open_tasks(),
		closed_tasks = closed_tasks(),
		username = session['username']
		)


@tasks_blueprint.route('/add_task/', methods=['GET','POST'])
@login_required
def new_task():
	error = None
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate():
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				datetime.datetime.utcnow(),
				'1',
				session['user_id']
				)
			db.session.add(new_task)
			db.session.commit()
			flash('New entry was successfully posted. Thanks.')
			return redirect(url_for('tasks.tasks'))
		else:
			return render_template('tasks.html', form=form, error=error, open_tasks=open_tasks(), closed_tasks=closed_tasks())
	return render_template('tasks.html', form=form, open_tasks=open_tasks(), closed_tasks=closed_tasks())
	

@tasks_blueprint.route('/mark_complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id or session['role'] == 'admin':
		task.update({"status": "0"})
		db.session.commit()
		flash("The task is complete. Nice.")
		return redirect(url_for('tasks.tasks'))
	else:
		flash("You can only update tasks that belong to you.")
		return redirect(url_for('tasks.tasks'))

@tasks_blueprint.route('/delete_task/<int:task_id>/')
@login_required
def delete_entry(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id or session['role'] == 'admin':
		task.delete()
		db.session.commit()
		flash('The task was deleted.')
		return redirect(url_for('tasks.tasks'))
	else:
		flash("You can only delete tasks that belong to you.")
		return redirect(url_for('tasks.tasks'))


