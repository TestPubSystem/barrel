#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import db
from data.result import Status, StepResult
from data.test import TestRevision


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))
    test_revision_id = db.Column(db.Integer, db.ForeignKey('test_revision.id'))
    step_results = db.relationship("StepResult", cascade="all")
    test_revision = db.relationship("TestRevision", uselist=False)
    suite_run_id = db.Column(db.Integer, db.ForeignKey("suite_run.id"), nullable=True)
    comment = db.Column(db.String(140), unique=False)
    finish_date = db.Column(db.DateTime)

    # attachments = None
    # author_id = None

    def to_map(self):
        return {
            "id": self.id,
            "status": self.status,
            "test_revision_id": self.test_revision_id,
            "step_statuses": self.step_statuses,
            "suite_run_id": self.suite_run_id,
            "comment": self.comment,
            "finish_date": self.finish_date,
        }


def create_from_test(test):
    run = TestRun()
    run.test_revision = test.last_revision
    for step in test.last_revision.steps:
        res = StepResult()
        res.step = step
        run.step_statuses.appen(res)
    return run
