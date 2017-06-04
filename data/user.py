#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import enum

from data import db


@enum.unique
class Role(enum.Enum):
    manager = "manager"
    tester = "tester"
    test_designer = "test_designer"
    admin = "admin"


class UserAuth(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=False)
    password_hash = db.Column(db.String(128), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # roles = db.Column(db.Enum(Role))
    login = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=True)
    # avatar =
    registration_date = db.Column(db.DateTime, default=db.func.now())
    blocked = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    user_auth = db.relationship(
        UserAuth,
        cascade="all",
        uselist=False,
    )

    def to_map(self):
        return {
            "login": self.login,
            "name": self.name
        }
