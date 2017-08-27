# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restplus import Api
import logging
from logging.handlers import RotatingFileHandler
import pymysql

pymysql.install_as_MySQLdb()

# Define the WSGI application object
app = Flask(__name__)

# Define Api application object
api = Api(app, version='0.5a', title='My3r',
    description='API do My3r',)

# Configurations
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add log handler
handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=100000, backupCount=50)
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    app.logger.error(error)
    return error

from app.mod_core import models
# from app.mod_auth import models
# from app.mod_events import models


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_core.controllers import mod_core as core_module, ns as ns_core
from app.mod_interacao.controllers import mod_interacao as interacao_module, ns as ns_interacao
from app.mod_interesse.controllers import mod_interesse as interesse_module, ns as ns_interesse
from app.mod_local.controllers import mod_local as local_module, ns as ns_local
# from app.mod_ import mod_ as _module, ns as ns_
# from app.mod_auth.controllers import mod_auth as auth_module, ns as ns_auth
# from app.mod_events.controllers import mod_event as event_module, ns as ns_event

# Register blueprint(s)
app.register_blueprint(core_module)
app.register_blueprint(interacao_module)
app.register_blueprint(interesse_module)
app.register_blueprint(local_module)

# Register API namespace(s)
api.add_namespace(ns_core)
api.add_namespace(ns_interacao)
api.add_namespace(ns_interesse)
api.add_namespace(ns_local)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.drop_all()
db.create_all()