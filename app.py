#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from data import db
from data import test
from flask import jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db.init_app(app)
db.app = app

db.create_all(app=app)


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


@app.route("/api/v1/tests/")
def get_tests(offset=0, limit=20):
    res = test.Test.query.offset(offset).limit(limit).all()
    print(res)
    return jsonify(data=[x.to_map() for x in res])


@app.route("/api/v1/tests/<int:test_id>")
def get_test(test_id):
    res = test.Test.query.get(test_id)
    print(res)
    return jsonify(data=res.to_map())


@app.route("/api/v1/tests/<int:test_id>/revisions/")
def get_test_revisions(test_id):
    res = test.TestRevision.query.filter_by(test_id=test_id).all()
    return jsonify(data=[x.to_map() for x in res])


@app.route("/api/v1/tests/<int:test_id>/revisions/<int:revision_id>", methods=["GET"])
@app.route("/api/v1/revisions/<int:revision_id>", methods=["GET"])
def get_test_revision(revision_id, test_id=None):
    res = test.TestRevision.get(revision_id)
    return jsonify(data=res.to_map())


@app.route("/api/v1/tests/<int:test_id>", methods=["PUT"])
def update_test(test_id):
    t = test.Test.query.get(test_id)
    data = request.get_json(force=True)
    rev = test.TestRevision.from_map(data)
    rev.test = t
    db.session.add(rev)
    db.session.commit()
    return jsonify(data=t.to_map())


@app.route("/api/v1/tests/<int:test_id>", methods=["DELETE"])
def delete_test(test_id):
    test.Test.query.filter(test.Test.id == test_id).delete()
    db.session.commit()
    return jsonify()


@app.route("/api/v1/tests/", methods=["POST"])
def create_test():
    data = request.get_json(force=True)
    rev = test.TestRevision.from_map(data)
    t = test.Test()
    rev.test = t
    db.session.add(rev)
    db.session.add(t)
    db.session.commit()
    return jsonify(data=t.to_map()), 201


app.run()
