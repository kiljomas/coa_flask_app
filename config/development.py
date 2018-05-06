import os

DEBUG = True

DB_SERVER = os.environ['DB_SERVER']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_DATABASE = os.environ['DB_DATABASE']
DB_PORT = os.environ['DB_PORT']

SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format( \
                            DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, \
                            DB_DATABASE))
