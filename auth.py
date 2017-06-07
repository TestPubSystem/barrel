#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug import security
from flask_jwt import JWT, _default_jwt_payload_handler

from data.user import User

jwt = JWT()


@jwt.authentication_handler
def authenticate(login, password):
    user = User.query.filter_by(login=login).one_or_none()
    if user \
            and user.confirmed \
            and not user.blocked \
            and user.user_auth \
            and security.check_password_hash(user.user_auth.password_hash, password):
        return user


@jwt.identity_handler
def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)


@jwt.jwt_payload_handler
def make_payload(idnt: User):
    res = _default_jwt_payload_handler(idnt)
    res.update({"login": idnt.login, "name": idnt.name})
    return res
