#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import enum
from werkzeug.utils import cached_property

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


class TestResult:
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


class SuiteRun:
    id = db.Column(db.Integer, primary_key=True)
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_revision.id'))
    start_date = db.Column(db.DateTime, default=db.func.now())
    finish_date = db.Column(db.DateTime)
    test_results = db.relationship("TestResult", cascade="all")
    # results = None  # type: list[TestResult]
    # author_id = None
