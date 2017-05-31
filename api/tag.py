#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify

from data import test, test_suite, tag
from data import db

tag_blueprint = Blueprint("tag", __name__)


@tag_blueprint.route("/", methods=["GET"])
def get_tags(offset=0, limit=20):
    res = tag.Tag.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@tag_blueprint.route("/", methods=["POST"])
def create_tag():
    data = request.get_json(force=True)
    res = tag.Tag()
    res.update_from_map(data)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@tag_blueprint.route("/<tag_name>", methods=["GET"])
def get_tag(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    return jsonify(data=res)


@tag_blueprint.route("/<tag_name>", methods=["DELETE"])
def delete_tag(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    db.session.delete(res)
    db.session.commit()
    return jsonify(data=None)


@tag_blueprint.route("/<tag_name>", methods=["PUT"])
def update_tag(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    data = request.get_json(force=True)
    res.update_from_map(data)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@tag_blueprint.route("/<tag_name>/testsuites", methods=["GET"])
def get_tag_test_suites(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    return jsonify(data=res.test_suites)


@tag_blueprint.route("/<tag_name>/tests", methods=["GET"])
def get_tag_tests(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    return jsonify(data=res.tests)
