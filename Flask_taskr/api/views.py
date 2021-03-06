from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response, request
from flask_restful import Api, Resource, abort, url_for
from flask_sqlalchemy import SQLAlchemy

from Flask_taskr import db, app
from Flask_taskr.models import Task


################
#### config ####
################


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


################
 # api classes #
################


class api_list_all_tasks(Resource):
    def get(self):
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
            code = 200
        return make_response(jsonify(items=json_results), code)


class api_list_individual_task(Resource):
    def get(self, task_id):
        result = db.session.query(Task).filter_by(task_id=task_id).first()
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
        else:
            result = {"error": "Element does not exist"}
            code = 404
            return make_response(jsonify(result), code)

class api_delete_a_task(Resource):
    def delete(self, task_id):
        task = db.session.query(Task).filter_by(task_id=task_id)
        task_name = task.first().name
        task.delete()
        db.session.commit()
        json_confirmation = {'deleted': task_name}
        code = 200
        return make_response(jsonify(json_confirmation), code)

class api_mark_complete_a_task(Resource):
    def put(self, task_id):
        task = db.session.query(Task).filter_by(task_id=task_id)
        task.update({"status":"0"})
        json_confirmation = {'marked complete': task.first().name}
        db.session.commit()
        code=200
        return make_response(jsonify(json_confirmation), code)




################
 # api routes #
################

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(api_list_all_tasks, '/api/v1/tasks')
api.add_resource(api_list_individual_task, '/api/v1/tasks/<int:task_id>')
api.add_resource(api_delete_a_task,'/api/v1/delete_task/<int:task_id>')
api.add_resource(api_mark_complete_a_task,'/api/v1/mark_complete/<int:task_id>')
