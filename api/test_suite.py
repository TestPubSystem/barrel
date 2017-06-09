#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt import jwt_required, current_identity

from data import test
from data import test_suite
from data import tag
from data import project
from data import db

test_suite_blueprint = Blueprint("testsuites", __name__)


@test_suite_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_test_suites(offset=0, limit=20):
    res = test_suite.TestSuite.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>", methods=["GET"])
@jwt_required()
def get_test_suite(test_suite_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>", methods=["DELETE"])
@jwt_required()
def delete_test_suite(test_suite_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    db.session.delete(res)
    db.session.commit()
    return jsonify(data=None)


@test_suite_blueprint.route("/<int:test_suite_id>", methods=["PUT"])
@jwt_required()
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
@jwt_required()
def create_test_suite():
    data = request.get_json(force=True)
    res = test_suite.TestSuite()
    project_id = data["project"]["id"]
    prj = project.Project.query.get(project_id)  # type: project.Project
    res.project = prj
    if "tags" in data:
        for tg in data["tags"]:
            res.tags.append(tag.Tag.query.filter_by(title=tg["title"]).one_or_none())
    res.update_from_map(data)
    res.author = current_identity
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>/tests/<int:test_id>", methods=["POST"])
@jwt_required()
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
@jwt_required()
def delete_test_suite_test(test_suite_id, test_id):
    res = test_suite.TestSuite.query.get(test_suite_id)
    if not res:
        return jsonify(error="No testsuite found"), 404
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    res.tests.remove(t)
    db.session.commit()
    return jsonify(data=res)


@test_suite_blueprint.route("/<int:test_suite_id>/tags/<tag_name>", methods=["POST"])
@jwt_required()
def add_tag(test_suite_id, tag_name):
    t = test_suite.TestSuite.query.get(test_suite_id)
    if not t:
        return jsonify(error="No test found"), 404
    tg = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not tg:
        return jsonify(error="No tagsuite found"), 404
    t.tags.append(tg)
    db.session.commit()
    return jsonify(data=t)


@test_suite_blueprint.route("/<int:test_suite_id>/tags/<tag_name>", methods=["DELETE"])
@jwt_required()
def delete_tag(test_suite_id, tag_name):
    t = test_suite.TestSuite.query.get(test_suite_id)
    if not t:
        return jsonify(error="No testsuite found"), 404
    tg = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not tg:
        return jsonify(error="No tag found"), 404
    t.tags.remove(tg)
    db.session.commit()
    return jsonify(data=t)
