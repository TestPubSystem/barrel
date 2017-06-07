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
    start_date = db.Column(db.DateTime, default=db.func.now())
    finish_date = db.Column(db.DateTime)
    test_runs = db.relationship("TestRun", cascade="all")  # type: list[TestRun]

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="suite_runs", foreign_keys=[author_id])  # type: User

    responsible_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    responsible = db.relationship("User", backref="responsible_suite_runs", foreign_keys=[responsible_id])  # type: User

    def to_map(self):
        return {
            "id": self.id,
            "test_suite_id": self.test_suite_id,
            "start_date": self.start_date,
            "finish_date": self.finish_date,
            "test_runs": self.test_runs,
            "author": self.author,
            "responsible": self.responsible
        }


def create_from_test_suite(test_suite: TestSuite, author: User, responsible: User):
    run = SuiteRun()
    run.author = author
    run.responsible = responsible
    run.test_suite_id = test_suite.id
    for test in test_suite.tests:
        res = data.test_run.create_from_test(test)
        run.test_runs.append(res)
    return run
