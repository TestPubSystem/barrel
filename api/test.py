#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt import jwt_required, current_identity

from data import test
from data import db
from data import tag
from data import project

test_blueprint = Blueprint("tests", __name__)


@test_blueprint.route("/")
@jwt_required()
def get_tests(offset=0, limit=20):
    res = test.Test.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@test_blueprint.route("/<int:test_id>")
@jwt_required()
def get_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    return jsonify(data=t)


@test_blueprint.route("/<int:test_id>/revisions/")
@jwt_required()
def get_test_revisions(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    return jsonify(data=t.revisions)


@test_blueprint.route("/<int:test_id>/revisions/<int:revision_id>", methods=["GET"])
@jwt_required()
def get_test_revision_by_test(revision_id, test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    res = test.TestRevision.query.get(revision_id)
    if not res:
        return jsonify(error="No revision found"), 404
    return jsonify(data=res)


@test_blueprint.route("/<int:test_id>/revisions/", methods=["POST"])
@jwt_required()
def update_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    data = request.get_json(force=True)
    rev = test.TestRevision()
    rev.update_from_map(data)
    rev.author = current_identity
    rev.test = t
    db.session.add(rev)
    db.session.commit()
    return jsonify(data=t)


@test_blueprint.route("/<int:test_id>", methods=["DELETE"])
@jwt_required()
def delete_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify()


@test_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_test():
    data = request.get_json(force=True)
    t = test.Test()
    project_id = data["project"]["id"]
    prj = project.Project.query.get(project_id)  # type: project.Project
    t.project = prj
    if "tags" in data:
        for tg in data["tags"]:
            t.tags.append(tag.Tag.query.filter_by(title=tg["title"]).one_or_none())
    rev = test.TestRevision()
    rev.update_from_map(data["last_revision"])
    rev.test = t
    rev.author = current_identity
    db.session.add(rev)
    db.session.add(t)
    db.session.commit()
    return jsonify(data=t), 201


@test_blueprint.route("/<int:test_id>/tags/<tag_name>", methods=["POST"])
@jwt_required()
def add_tag(test_id, tag_name):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    tg = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not tg:
        return jsonify(error="No tag found"), 404
    t.tags.append(tg)
    db.session.commit()
    return jsonify(data=t)


@test_blueprint.route("/<int:test_id>/tags/<tag_name>", methods=["DELETE"])
@jwt_required()
def delete_tag(test_id, tag_name):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    tg = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not tg:
        return jsonify(error="No tag found"), 404
    t.tags.remove(tg)
    db.session.commit()
    return jsonify(data=t)
