import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)+ '../..'+'/Flask_taskr_project')) 
# MUST RUN TEST WITH COVERAGE, TO RUN WITHOUT COVERAGE REMOVE +'Flask_taskr_project'
import unittest
from Flask_taskr import app, db
from Flask_taskr._config import basedir
from Flask_taskr.models import Task, User


TEST_DB = 'test.db'

from test_tasks import TasksTests
from test_users import UsersTests
from test_main import MainTests
from test_api import APITests


unittest.main()