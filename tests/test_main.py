import os
import unittest
import sys
sys.path.append(os.path.dirname(__file__)+'../..')
from Flask_taskr import app, db
from Flask_taskr._config import basedir
from Flask_taskr.models import User

TEST_DB = 'test.db'

class MainTests(unittest.TestCase):
	
	############################
	#### setup and teardown ####
	############################

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()
		self.assertEquals(app.debug, False)
		
	def tearDown(self):
		db.session.remove()
		db.drop_all()

	########################
	#### helper methods ####
	########################

	def login(self, name, password):
		return self.app.post('/', data=dict(
			username=name, password=password), follow_redirects=True)

	###############
	#### tests ####
	###############

	def test_404_error(self):
		response = self.app.get('/this-route-does-not-exist/')
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'Sorry. There\'s nothing here.', response.data)

	def test_500_error(self):
		bad_user=User(
			username='Jeremy',
			email='jeremy@realpython.com',
			password='django'
			)
		db.session.add(bad_user)
		db.session.commit()
		self.assertRaises(ValueError, self.login, 'Jeremy', 'django')
		try:
			response = self.login('Jeremy', 'django')
			self.assertEquals(response.status_code, 500)
		except ValueError:
			pass
	
	def test_index(self):
		"""Ensureflask was set up correctly."""
		response = self.app.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
	unittest.main()