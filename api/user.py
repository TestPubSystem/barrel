#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask_jwt import jwt_required, current_identity

from data import user

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=["GET"])
#@jwt_required()
def get_users(offset=0, limit=20):
    res = user.User.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@user_blueprint.route("/self", methods=["GET"])
@jwt_required()
def get_self():
    return jsonify(data=current_identity)


@user_blueprint.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    res = user.User.query.get(user_id)
    if not res:
        return "User not found", 404
    return jsonify(data=res)
