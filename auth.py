#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug import security
from data import db
from data.user import User, UserAuth


def authenticate(login, password):
    user = User.query.filter_by(login=login).one_or_none()
    if security.check_password_hash(user.user_auth.password_hash, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)
