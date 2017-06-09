#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import db
from data.test_suite import TestSuite
from data.test import Test


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    desc = db.Column(db.String(140))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="projects", foreign_keys=[author_id])  # type: User
    creation_date = db.Column(db.DateTime, default=db.func.now())
    tests = db.relationship("Test", backref="project", cascade="all", lazy="dynamic")  # type: Test
    test_suites = db.relationship("TestSuite", backref="project", cascade="all", lazy="dynamic")  # type: TestSuite
    test_runs = db.relationship("TestRun", backref="project", cascade="all", lazy="dynamic")  # type: TestRun
    suite_runs = db.relationship("SuiteRun", backref="project", cascade="all", lazy="dynamic")  # type: SuiteRun

    def to_map(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "author": self.author,
            "creation_date": self.creation_date,
        }

    def update_from_map(self, data):
        self.name = data.get("name", self.name)
        self.desc = data.get("desc", self.desc)
