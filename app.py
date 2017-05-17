#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from data import db
from data import test

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db.init_app(app)
db.app = app

# db.create_all(app=app)
#
# t = test.Test()
# r = test.TestRevision()
# r.test = t
# r.title = "Title 1"
#
# for i in range(10):
#     r.steps.append(test.Step("Step %s" % i))
#
# r2 = test.TestRevision()
# r2.test = t
#
# db.session.add(r2)
# db.session.add(r)
# db.session.add(t)
# db.session.commit()

t = test.Test.query.one()
print("Test got")
print(t.revisions)
