#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt import jwt_required

from data import tag
from data import db

tag_blueprint = Blueprint("tag", __name__)


@tag_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_tags(offset=0, limit=20):
    res = tag.Tag.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@tag_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_tag():
    data = request.get_json(force=True)
    res = tag.Tag()
    res.update_from_map(data)
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@tag_blueprint.route("/<tag_name>", methods=["GET"])
@jwt_required()
def get_tag(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    return jsonify(data=res)


@tag_blueprint.route("/<tag_name>", methods=["DELETE"])
@jwt_required()
def delete_tag(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    db.session.delete(res)
    db.session.commit()
    return jsonify(data=None)


@tag_blueprint.route("/<tag_name>", methods=["PUT"])
@jwt_required()
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
@jwt_required()
def get_tag_test_suites(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    return jsonify(data=res.test_suites)


@tag_blueprint.route("/<tag_name>/tests", methods=["GET"])
@jwt_required()
def get_tag_tests(tag_name):
    res = tag.Tag.query.filter_by(title=tag_name).one_or_none()
    if not res:
        return jsonify(error="No tag found"), 404
    return jsonify(data=res.tests)
