#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import db
from data.result import Status, StepResult
from data.test import TestRevision, Test

import datetime


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
            "step_results": self.step_results,
            "suite_run_id": self.suite_run_id,
            "comment": self.comment,
            "finish_date": self.finish_date,
        }

    def update_from_map(self, data):
        self.comment = data.get("comment", self.comment)
        self.status = data.get("status", self.status)
        if self.status:
            self.finish_date = datetime.datetime.now()
        self.suite_run_id = data.get("suite_run_id", self.suite_run_id)


def create_from_test_revision(revision: TestRevision):
    run = TestRun()
    run.test_revision = revision
    for step in revision.steps:
        res = StepResult()
        res.step = step
        run.step_results.append(res)
    return run


def create_from_test(test: Test):
    return create_from_test_revision(test.last_revision)
