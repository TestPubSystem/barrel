#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import enum
from data import db


@enum.unique
class StepType(enum.Enum):
    step = "step"
    expected_result = "expected_result"


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(StepType))
    text = db.Column(db.String(140), unique=False)
    order_number = db.Column(db.Integer)
    test_revision_id = db.Column(db.Integer, db.ForeignKey('test_revision.id'))

    # attachments = None  # type: list

    def __init__(self, text=None):
        self.text = text

    def to_map(self):
        return {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "order_number": self.order_number,
        }

    @classmethod
    def from_map(cls, x):
        self = Step()
        self.update_from_map(x)
        return self

    def update_from_map(self, x):
        self.type = x.get("type")
        self.text = x.get("text")
        self.order_number = x.get("order_number")


class TestRevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    desc = db.Column(db.String(140), unique=False)  # type: str
    pre_condition = db.Column(db.String(140), unique=False)  # type: str
    post_condition = db.Column(db.String(140), unique=False)  # type: str
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

    steps = db.relationship(
        'Step',
        cascade="all"
    )

    def __init__(self):
        self.steps = []

    # parameters = None  # type: list[str]
    # author_id = None
    # creation_date = None  # type: datetime.datetime

    def to_map(self):
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "pre_condition": self.pre_condition,
            "post_condition": self.post_condition,
            "steps": [x.to_map() for x in self.steps] if self.steps else None,
        }

    @classmethod
    def from_map(cls, x):
        self = TestRevision()
        self.update_from_map(x)
        return self

    def update_from_map(self, x):
        self.test_id = x.get("test_id")
        self.title = x.get("title")
        self.desc = x.get("desc")
        self.pre_condition = x.get("pre_condition")
        self.post_condition = x.get("post_condition")
        steps = x.get("steps")
        if steps:
            self.steps.extend([Step.from_map(y) for y in steps])


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @property
    def last_revision(self):
        return TestRevision.query.filter_by(test_id=self.id).order_by(TestRevision.id.desc()).limit(1).first()

    revisions = db.relationship(
        'TestRevision',
        backref=db.backref('test'),
        cascade="all",
        lazy = 'dynamic',
    )
    # tags = None  # type: list[str]
    # author_id = None
    # creation_date = None  # type: datetime.datetime

    def to_map(self):
        last_revision = self.last_revision
        return {
            "id": self.id,
            "last_revision": last_revision.to_map() if last_revision else None
        }


test_suite_tests = db.Table()


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    tests = None  # type: list[Test]
    tags = None  # type: list[str]
    author_id = None
    creation_date = None  # type: datetime.datetime
