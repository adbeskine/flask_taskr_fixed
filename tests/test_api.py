# tests/test_api.py


import os
import unittest
from datetime import date
import sys
sys.path.append(os.path.dirname(__file__)+'../..')
from Flask_taskr import app, db
from Flask_taskr._config import basedir
from Flask_taskr.models import Task
from sqlalchemy.sql import exists


TEST_DB = 'test.db'


class APITests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def add_tasks(self):
        db.session.add(
            Task(
                "Run around in circles",
                date(2015, 10, 22),
                10,
                date(2015, 10, 5),
                1,
                1
            )
        )
        db.session.commit()

        db.session.add(
            Task(
                "Purchase Real Python",
                date(2016, 2, 23),
                10,
                date(2016, 2, 7),
                1,
                1
            )
        )
        db.session.commit()

    ###############
    #### tests ####
    ###############

    def test_collection_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Run around in circles', response.data)
        self.assertIn(b'Purchase Real Python', response.data)

    def test_resource_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Purchase Real Python', response.data)
        self.assertNotIn(b'Run around in circles', response.data)

    def test_invalid_resource_endpoint_returns_error(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/209', follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Element does not exist', response.data)

    def test_api_can_delete_tasks(self):
        self.add_tasks()
        response = self.app.delete('api/v1/delete_task/1')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn(1, db.session.query(Task).filter_by(task_id=1))
        self.assertTrue(db.session.query(exists().where(Task.task_id==2)).scalar())

    def test_api_can_mark_complete_tasks(self):
        self.add_tasks()
        response = self.app.put('api/v1/mark_complete/1')
        self.assertEquals(response.status_code, 200)
        completed_task = db.session.query(Task).filter_by(task_id=1).first()
        self.assertTrue(completed_task.status == 0)
        untouched_task = db.session.query(Task).filter_by(task_id=2).first()
        self.assertTrue(untouched_task.status==1)
        self.assertEquals(response.mimetype, 'application/json')



unittest.main()