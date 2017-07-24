import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE = 'flasktaskr.db'
DEBUG = False
WTF_CSRF_ENABLED = True
CSRF_ENABLED = True
SECRET_KEY = 'O.(F2]N$f58=K&xhZz.8/Du{YmJz>x'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH