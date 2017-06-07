#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import db
from data.test_suite import TestSuite
from data.test_run import TestRun
import data.test_run

class SuiteRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'))
    start_date = db.Column(db.DateTime, default=db.func.now())
    finish_date = db.Column(db.DateTime)
    test_runs = db.relationship("TestRun", cascade="all")

    # author_id = None

    def to_map(self):
        return {
            "id": self.id,
            "test_suite_id": self.test_suite_id,
            "start_date": self.start_date,
            "finish_date": self.finish_date,
            "test_runs": self.test_runs,
        }


def create_from_test_suite(test_suite: TestSuite):
    run = SuiteRun()
    run.test_suite_id = test_suite.id
    for test in test_suite.tests:
        res = data.test_run.create_from_test(test)
        run.test_runs.append(res)
    return run
