#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from data import db

from api.project import project_blueprint
from api.test import test_blueprint
from api.test_suite import test_suite_blueprint
from api.tag import tag_blueprint
from api.suite_run import suite_run_blueprint
from api.test_run import test_run_blueprint
from api.step_result import step_result_blueprint
from api.user import user_blueprint

from db_json_encoder import CustomJSONEncoder

from flask_cors import CORS
from auth import jwt

import auth
import init

DEBUG = True  # FIXME remove in production

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["JWT_AUTH_USERNAME_KEY"] = "login"
app.config["JWT_AUTH_URL_RULE"] = "/api/v1/auth"
app.config['SECRET_KEY'] = 'super-secret'  # FIXME generate on first start
app.json_encoder = CustomJSONEncoder

db.init_app(app)
db.app = app

jwt.init_app(app)
jwt.app = app

init.deploy(app)

if DEBUG:
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(project_blueprint, url_prefix="/api/v1/projects")
app.register_blueprint(test_blueprint, url_prefix="/api/v1/tests")
app.register_blueprint(test_suite_blueprint, url_prefix="/api/v1/testsuites")
app.register_blueprint(tag_blueprint, url_prefix="/api/v1/tags")
app.register_blueprint(suite_run_blueprint, url_prefix="/api/v1/suiteruns")
app.register_blueprint(test_run_blueprint, url_prefix="/api/v1/testruns")
app.register_blueprint(step_result_blueprint, url_prefix="/api/v1/stepresults")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/users")

if __name__ == "__main__":
    app.run()
