#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify

from data import user
from data import db

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=["GET"])
def get_users(offset=0, limit=20):
    res = user.User.query.offset(offset).limit(limit).all()
    return jsonify(data=res)
