from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response
from flask_restful import Api, Resource, abort
from flask_taskr import db
from Flask_taskr.models import Task





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


def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())

def abort_if_task_not_exist(task_id):
	if task_id not in db.session.query(Task).filter_by(task_id=task_id.first):
			abort(404, message = "error: task does not exist")

################
#### routes ####
################

# @api_blueprint.route('/api/v1/tasks/')


# @api_blueprint.route('/api/v1/tasks/<int:task_id>')


class Get_all_tasks(Resource):
	def get_all_tasks(self):
		results = db.session.query(Task).limit(10).offset(0).all()
		json_results = []
		for result in results:
			data = {
			'task_id': result.task_id,
			'task name': result.name,
			'due date': str(result.due_date),
			'priority': result.priority,
			'posted date': str(result.posted_date),
			'status': result.status,
			'user id': result.user_id
			}
			json_results.append(data)
		return jsonify(items=json_results)

   

class get_individual_task(resource):
	def get_individual_task(self, task_id):
		result = db.session.query(Task).filter_by(task_id=task_id).first()
		abort_if_task_not_exist(task_id)
		if result:
			json_result = {
			'task_id':result.task_id,
			'task name': result.name,
			'due_date':str(result.due_date),
			'priority': result.priority,
			'posted date':str(result.posted_date),
			'status':result.status,
			'user id':result.user_id
			}
		code = 200
		return make_response(jsonify(json_result), code)


		