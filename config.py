# Statement for enabling the development environment
# Enabling the development environment
# DEBUG = True
# DB_USER = 'postgres'
# DB_PASS = 'postgres'
# DB_HOST = 'localhost'
# # DB_PORT = '80'
# DB_NAME = 'my3r'

DB_HOST = "ec2-23-23-225-12.compute-1.amazonaws.com"
DB_PORT = "5432"
DB_USER = "vxvbyvagnjoblp"
DB_PASS = "39b8c9d6d9b7b22121edd0cd4abeb106454cd6157cf22ade266f7c920a2ae6ed"
DB_NAME = "d87hs6012pbvdm"

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'postgres://'+DB_USER+':'+DB_PASS+'@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "thesecretsss"

LOGGING_FORMAT = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
LOGGING_LOCATION = 'logs/error.log'