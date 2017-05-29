#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify

from data import test
from data import db
from data import tag

test_blueprint = Blueprint("tests", __name__)


@test_blueprint.route("/")
def get_tests(offset=0, limit=20):
    res = test.Test.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@test_blueprint.route("/<int:test_id>")
def get_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    return jsonify(data=t)


@test_blueprint.route("/<int:test_id>/revisions/")
def get_test_revisions(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    return jsonify(data=t.revisions)


@test_blueprint.route("/<int:test_id>/revisions/<int:revision_id>", methods=["GET"])
def get_test_revision_by_test(revision_id, test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    res = test.TestRevision.query.get(revision_id)
    if not res:
        return jsonify(error="No revision found"), 404
    return jsonify(data=res)


@test_blueprint.route("/<int:test_id>/revisions", methods=["POST"])
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


@test_blueprint.route("/<int:test_id>", methods=["DELETE"])
def delete_test(test_id):
    t = test.Test.query.get(test_id)
    if not t:
        return jsonify(error="No test found"), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify()


@test_blueprint.route("/", methods=["POST"])
def create_test():
    data = request.get_json(force=True)
    rev = test.TestRevision.from_map(data["last_revision"])
    t = test.Test()
    rev.test = t
    db.session.add(rev)
    db.session.add(t)
    db.session.commit()
    return jsonify(data=t), 201


@test_blueprint.route("/<int:test_id>/tags/<tag_name>", methods=["POST"])
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
