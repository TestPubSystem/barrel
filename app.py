#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from data import db
from data import test
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db.init_app(app)
db.app = app


#
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


# t = test.Test.query.one()
# print("Test got")
# print(t.last_revision)


@app.route("/api/v1/tests/")
def get_tests(offset=0, limit=20):
    res = test.Test.query.offset(offset).limit(limit).all()
    print(res)
    return jsonify(data=[x.to_map() for x in res])


@app.route("/api/v1/tests/<int:test_id>")
def get_test(test_id):
    res = test.Test.query.filter_by(id=test_id).limit(1).one()
    print(res)
    return jsonify(data=res.id)


@app.route("/api/v1/tests/<int:test_id>/revisions/")
def get_test_revisions(test_id):
    res = test.TestRevision.query.filter_by(test_id=test_id).all()
    print(res)
    return jsonify(data=[{"id": x.id, "title": x.title} for x in res])


app.run()
