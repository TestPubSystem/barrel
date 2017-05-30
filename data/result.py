#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum

from data.test import TestRevision, Step
from data.test_suite import TestSuite
from data import db


@enum.unique
class Status(enum.Enum):
    success = "success"
    partial = "partial"
    failed = "failed"
    blocked = "blocked"


class StepResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'))
    step = db.relationship(
        'Step'
    )
    completion_date = db.Column(db.DateTime, default=db.func.now())
    comment = db.Column(db.String(140), unique=False)

    # attachments = None

    def to_map(self):
        return {
            "id": self.id,
            "status": self.status,
            "step_id": self.step_id,
            "step": self.step,
            "completion_date": self.completion_date,
            "comment": self.comment
        }

    def update_from_map(self, data):
        self.status = data.get("status", self.status)
        self.step_id = data.get("step_id", self.step_id)
        self.completion_date = data.get("completion_date", self.completion_date)
        self.comment = data.get("comment", self.comment)


class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))
    test_revision_id = db.Column(db.Integer, db.ForeignKey('test_revision.id'))
    step_statuses = db.relationship("StepResult", cascade="all")
    test_revision = db.relationship("TestRevision", lazy="dynamic")
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


class SuiteRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_revision.id'))
    start_date = db.Column(db.DateTime, default=db.func.now())
    finish_date = db.Column(db.DateTime)
    test_results = db.relationship("TestResult", cascade="all")

    # author_id = None

    def to_map(self):
        return {
            "id": self.id,
            "test_suite_id": self.test_suite_id,
            "start_date": self.start_date,
            "finish_date": self.finish_date,
            "test_results": self.test_results,
        }
