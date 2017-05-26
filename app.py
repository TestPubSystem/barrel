#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from data import db
from api.test import test_blueprint
from api.test_suite import test_suite_blueprint
from api.tag import tag_blueprint
from db_json_encoder import CustomJSONEncoder

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.json_encoder = CustomJSONEncoder
db.init_app(app)
db.app = app

db.create_all(app=app)

app.register_blueprint(test_blueprint, url_prefix="/api/v1/tests")
app.register_blueprint(test_suite_blueprint, url_prefix="/api/v1/testsuites")
app.register_blueprint(tag_blueprint, url_prefix="/api/v1/tags")

if __name__ == "__main__":
    app.run()
