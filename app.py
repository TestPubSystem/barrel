#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from data import db
from data import test, test_suite
from flask import jsonify, request
from db_json_encoder import CustomJSONEncoder

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.json_encoder = CustomJSONEncoder
db.init_app(app)
db.app = app

db.create_all(app=app)


@app.route("/api/v1/tests/")
def get_tests(offset=0, limit=20):
    res = test.Test.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@app.route("/api/v1/tests/<int:test_id>")
def get_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    return jsonify(data=t)


@app.route("/api/v1/tests/<int:test_id>/revisions/")
def get_test_revisions(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    return jsonify(data=t.revisions)


@app.route("/api/v1/tests/<int:test_id>/revisions/<int:revision_id>", methods=["GET"])
def get_test_revision_by_test(revision_id, test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    res = test.TestRevision.query.get(revision_id)
    if not res:
        return jsonify(error="No revision found"), 404
    return jsonify(data=res)


@app.route("/api/v1/revisions/<int:revision_id>", methods=["GET"])
def get_test_revision(revision_id):
    res = test.TestRevision.query.get(revision_id)
    if not res:
        return jsonify(error="No revision found"), 404
    return jsonify(data=res)


@app.route("/api/v1/tests/<int:test_id>", methods=["PUT"])
def update_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    data = request.get_json(force=True)
    rev = test.TestRevision.from_map(data)
    rev.test = t
    db.session.add(rev)
    db.session.commit()
    return jsonify(data=t)


@app.route("/api/v1/tests/<int:test_id>", methods=["DELETE"])
def delete_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    db.session.delete(t)
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
    return jsonify(data=t), 201


@app.route("/api/v1/testsuites/", methods=["GET"])
def get_test_suites(offset=0, limit=20):
    res = test_suite.TestSuite.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@app.route("/api/v1/testsuites/<int:test_suite_id>", methods=["GET"])
def get_test_suite(test_suite_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    return jsonify(data=res)


@app.route("/api/v1/testsuites/", methods=["POST"])
def create_test_suite():
    data = request.get_json(force=True)
    res = test_suite.TestSuite.from_map(data)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@app.route("/api/v1/testsuites/<int:test_suite_id>/tests/<int:test_id>/", methods=["POST"])
def add_test_suite_test(test_suite_id, test_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    t = test.Test.query.get(test_id)
    res.tests.append(t)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


if __name__ == "__main__":
    app.run()
