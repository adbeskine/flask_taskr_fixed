from Flask_taskr import db
import datetime
from sqlalchemy import UniqueConstraint

class Task(db.Model):

	__tablename__ = "tasks"

	task_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	due_date = db.Column(db.Date, nullable=False)
	priority = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())

	def __init__(self, name, due_date, priority, posted_date, status, user_id):

		self.name = name
		self.due_date = due_date
		self.priority = priority
		self.status = status
		self.posted_date = posted_date
		self.user_id = user_id
	def __repr__(self):
		return '<name {0}>'.format(self.name)


class User(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	tasks = db.relationship('Task', backref='poster')
	role = db.Column(db.String, default='user')
	

	def __init__(self, username=None, password=None, email=None, role=None):
		self.username = username
		self.password = password
		self.email = email
		self.role = role

	def __repr__(self):
		return '<user {0}>'.format(self.username)