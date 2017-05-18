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
    test_revision = db.relationship('TestRevision', backref=db.backref('steps', lazy='dynamic'))
    # attachments = None  # type: list

    def __init__(self, text):
        self.text = text

    def to_map(self):
        return {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "order_number": self.order_number
        }


class TestRevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    desc = db.Column(db.String(140), unique=False)  # type: str
    pre_condition = db.Column(db.String(140), unique=False)  # type: str
    post_condition = db.Column(db.String(140), unique=False)  # type: str
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    test = db.relationship('Test')
    # parameters = None  # type: list[str]
    # author_id = None
    # creation_date = None  # type: datetime.datetime

    def to_map(self):
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "pre_condition": self.pre_condition,
            "post_condition": self.post_condition
        }


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @property
    def last_revision(self):
        return TestRevision.query.filter_by(test_id=self.id).order_by(TestRevision.id).limit(1).first()
    # revisions = db.relationship('TestRevision', uselist=True, lazy="dynamic")
    # last_revision = TestRevision.query.filter_by(test_id=id).order_by(TestRevision.id).limit(1).first()
    # tags = None  # type: list[str]
    # author_id = None
    # creation_date = None  # type: datetime.datetime

    def to_map(self):
        return {
            "id": self.id,
            "last_revision": self.last_revision.to_map() if self.last_revision else None
        }


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = None  # type: str
    tests = None  # type: list[Test]
    tags = None  # type: list[str]
    author_id = None
    creation_date = None  # type: datetime.datetime
