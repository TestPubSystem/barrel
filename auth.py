#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug import security
from data.user import User


def authenticate(login, password):
    user = User.query.filter_by(login=login).one_or_none()
    if user \
            and user.confirmed \
            and not user.blocked \
            and user.user_auth \
            and security.check_password_hash(user.user_auth.password_hash, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)
