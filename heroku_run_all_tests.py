import unittest
from Flask_taskr import app, db
from Flask_taskr._config import basedir
from Flask_taskr.models import Task, User


TEST_DB = 'test.db'

from tests.test_tasks import TasksTests
from tests.test_users import UsersTests
from tests.test_main import MainTests


unittest.main()