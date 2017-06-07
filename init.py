#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data.user import UserAuth, User
from data import db

from werkzeug.security import generate_password_hash


def deploy(app):
    db.create_all(app=app)
    if not db.session.query(User.id).count():
        u = User()
        u.name = "Root User"
        u.login = "root"
        u.confirmed = True
        u.blocked = False
        u.user_auth = UserAuth()
        u.user_auth.password_hash = generate_password_hash("password")

        db.session.add(u)
        db.session.commit()
        # end FIXME
