import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

	# ---------------- HELPER METHODS ------------------ # 

	def login(self, name, password):
		return self.app.post('/', data = dict(username = name, password = password), follow_redirects=True)

	def register(self, username, email, password, confirm):
		return self.app.post('/register', data=dict(username=username, email=email, password=password, confirm=confirm), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def create_user(self, name, email, password):
		new_user = User(username=name, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

	def create_task(self):
		return self.app.post('/add_task/', data=dict( name='go to the bank', due_date="10/08/16", priority='1', posted_date='10/08/16', status=1), follow_redirects=True)

	# -------------------------------------------------- #

	# -------- SETUP AND TEARDOWN --------------------- #

	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()


	#executed after each test
	def tearDown(self):
		db.session.remove()
		db.drop_all()
	# ------------------------------------------- #
	


	def test_form_is_present(self): # users
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please login to access your task list', response.data)	

	def test_users_cannot_login_unless_registered(self): # users
		response = self.login('foo', 'bar')
		self.assertIn(b'Invalid username or password.', response.data)

	def test_insert_new_user_data_into_database(self): # users
		new_user = User("michael", "michael@mherman.org", "michaelherman")
		db.session.add(new_user)
		db.session.commit()
		test = db.session.query(User).all()
		for t in test:
			t.username
		assert t.username == "michael"

	def test_users_can_login(self): # users
		self.register('Michael', 'michael@realpython.com', 'python', 'python')
		response = self.login('Michael', 'python')
		self.assertIn(b'Welcome!', response.data)

	def test_invalid_form_data(self): # users
		self.register('Michael', 'michael@realpython.com', 'python', 'python')
		response = self.login('alert("alert box!");', 'foo')
		self.assertIn(b'Invalid username or password.', response.data)

	def test_form_is_present_on_register_page(self): # users
		response = self.app.get('/register')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please register to access the task list.', response.data)

	def test_user_registration_via_register_form(self): # users
		self.app.get('/register', follow_redirects=True)
		response = self.register('Michael', 'michael@realpython.com', 'python', 'python')
		self.assertIn(b'New user registered', response.data)

	def test_logged_in_users_can_logout(self): # users
		self.register('Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
		self.login('Fletcher', 'python101')
		response = self.logout()
		self.assertIn(b'Goodbye!', response.data)

	def test_not_logged_in_users_cannot_logout(self): # users
		response = self.logout()
		self.assertNotIn(b'Goodbye!', response.data)

	def test_logged_in_users_can_access_tasks_page(self): # tasks
		self.register('Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
		self.login('Fletcher', 'python101')
		response = self.app.get('/tasks/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Add a new task:', response.data)

	def test_not_logged_in_users_cannot_access_tasks_page(self): # tasks
		response = self.app.get('/tasks/', follow_redirects=True)
		self.assertIn(b'You need to login first.', response.data)

	def test_users_can_add_tasks(self): # tasks
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks/', follow_redirects=True)
		response=self.create_task()
		self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

	def test_users_cannot_add_tasks_when_error(self): # tasks
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks/', follow_redirects=True)
		response = self.app.post('/add_task/', data=dict(
			name = 'go to the bank',
			due_date= '',
			priority='1',
			posted_date='02/05/2014',
			status='1'), follow_redirects=True)
		self.assertIn(b'This field is required', response.data)

	def test_users_can_complete_tasks(self): # tasks
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks/', follow_redirects=True)
		self.create_task()
		response=self.app.get("/mark_complete/1/", follow_redirects=True)
		self.assertIn(b'the task was marked as complete', response.data)

	def test_users_can_delete_tasks(self): #tasks
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get("/delete_task/1/", follow_redirects=True)
		self.assertIn(b'The task was deleted', response.data)

	def test_users_cannot_complete_tasks_that_are_not_created_by_them(self): # tasks
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
		self.login('Fletcher', 'python101')
		self.app.get('/tasks/', follow_redirects=True)
		response = self.app.get("/mark_complete/1/", follow_redirects=True)
		self.assertNotIn(b'the task was marked as complete', response.data)



if __name__ == "__main__":
	unittest.main()