#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify

from data import test, test_suite
from data import db

test_suite_blueprint = Blueprint("testsuites", __name__)


@test_suite_blueprint.route("/", methods=["GET"])
def get_test_suites(offset=0, limit=20):
    res = test_suite.TestSuite.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>", methods=["GET"])
def get_test_suite(test_suite_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    return jsonify(data=res)

@test_suite_blueprint.route("/<int:test_suite_id>", methods=["DELETE"])
def delete_test_suite(test_suite_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    db.session.delete(res)
    db.session.commit()
    return jsonify(data=None)


@test_suite_blueprint.route("/<int:test_suite_id>", methods=["PUT"])
def update_test_suite(test_suite_id):
    res = test_suite.TestSuite.query.get(test_suite_id)  # type: test_suite.TestSuite
    if not res:
        return jsonify(error="No testsuite found"), 404
    data = request.get_json(force=True)
    res.update_from_map(data)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@test_suite_blueprint.route("/", methods=["POST"])
def create_test_suite():
    data = request.get_json(force=True)
    res = test_suite.TestSuite.from_map(data)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>/tests/<int:test_id>", methods=["POST"])
def add_test_suite_test(test_suite_id, test_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    res.tests.append(t)
    db.session.commit()
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>/tests/<int:test_id>", methods=["DELETE"])
def delete_test_suite_test(test_suite_id, test_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    t = test.Test.query.get(test_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    res.tests.remove(t)
    db.session.commit()
    return jsonify(data=res)
    