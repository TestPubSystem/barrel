#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import enum
import random
import string

from data import db


@enum.unique
class Role(enum.Enum):
    manager = "manager"
    tester = "tester"
    test_designer = "test_designer"
    admin = "admin"


def gen_salt():
    return "".join(random.choice(string.ascii_letters) for i in range(63))


class UserAuth(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    salt = db.Column(db.String(64), nullable=False, default=gen_salt)
    password_sha256 = db.Column(db.String(64), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.Enum(Role))
    login = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    # avatar =
    registration_date = db.Column(db.DateTime, default=db.func.now())
    blocked = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
