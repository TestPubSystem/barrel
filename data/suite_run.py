#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import db
from data.test_suite import TestSuite
from data.test_run import TestRun
from data.user import User
import data.test_run


class SuiteRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    creation_date = db.Column(db.DateTime, default=db.func.now())
    finish_date = db.Column(db.DateTime)
    test_runs = db.relationship("TestRun", cascade="all")  # type: list[TestRun]

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="suite_runs", foreign_keys=[author_id])  # type: User

    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    assignee = db.relationship("User", backref="assigned_suite_runs", foreign_keys=[assignee_id])  # type: User

    def to_map(self):
        return {
            "id": self.id,
            "test_suite_id": self.test_suite_id,
            "creation_date": self.creation_date,
            "finish_date": self.finish_date,
            "test_runs": self.test_runs,
            "author": self.author,
            "assignee": self.assignee,
            "project": self.project,
        }


def create_from_test_suite(test_suite: TestSuite, author: User, assignee: User):
    run = SuiteRun()
    run.author = author
    run.assignee = assignee
    run.test_suite_id = test_suite.id
    run.project_id = test_suite.project_id
    for test in test_suite.tests:
        res = data.test_run.create_from_test(test, author, assignee)
        run.test_runs.append(res)
    return run
