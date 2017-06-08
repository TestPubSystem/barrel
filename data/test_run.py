#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import db
from data.result import Status, StepResult
from data.test import TestRevision, Test
from data.user import User

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
    creation_date = db.Column(db.DateTime, default=db.func.now())

    # attachments = None
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="test_runs", foreign_keys=[author_id])  # type: User

    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    assignee = db.relationship("User", backref="assigned_test_runs", foreign_keys=[assignee_id])  # type: User

    def to_map(self):
        return {
            "id": self.id,
            "status": self.status,
            "test_revision_id": self.test_revision_id,
            "step_results": self.step_results,
            "suite_run_id": self.suite_run_id,
            "comment": self.comment,
            "finish_date": self.finish_date,
            "author": self.author,
            "assignee": self.assignee,
            "creation_date": self.creation_date,
        }

    def update_from_map(self, data):
        self.comment = data.get("comment", self.comment)
        old_status = self.status
        self.status = data.get("status", self.status)
        if self.status != old_status:
            self.finish_date = datetime.datetime.now()
        if "assignee" in data:
            assignee_id = data["assignee"].get("id")
            self.assignee = User.query.get(assignee_id) if assignee_id else None
        self.suite_run_id = data.get("suite_run_id", self.suite_run_id)


def create_from_test_revision(revision: TestRevision, author: User, assignee: User):
    run = TestRun()
    run.test_revision = revision
    run.author = author
    run.assignee = assignee
    for step in revision.steps:
        res = StepResult()
        res.step = step
        run.step_results.append(res)
    return run


def create_from_test(test: Test, author: User, assignee: User):
    return create_from_test_revision(test.last_revision, author, assignee)
