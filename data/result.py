#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
import datetime

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
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_run.id'))
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
            "test_run_id": self.test_run_id,
            "step": self.step,
            "completion_date": self.completion_date,
            "comment": self.comment
        }

    def update_from_map(self, data):
        old_status = self.status
        self.status = data.get("status", self.status)
        if self.status != old_status:
            self.completion_date = datetime.datetime.now()
        self.comment = data.get("comment", self.comment)
