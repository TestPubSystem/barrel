#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
from data import db
from data.tag import Tag
from data.user import User
from werkzeug.utils import cached_property

test_tags = db.Table(
    "test_tags",
    db.Column("test_id", db.Integer, db.ForeignKey('test.id'), nullable=False),
    db.Column("tag_id", db.Integer, db.ForeignKey('tag.id'), nullable=False),
    db.UniqueConstraint("test_id", "tag_id", name="uix_test_tags")
)


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

    def update_from_map(self, x):
        self.type = x.get("type", self.type)
        self.text = x.get("text", self.text)
        self.order_number = x.get("order_number", self.order_number)


@enum.unique
class TestState(enum.Enum):
    deptecated = "deprecated"
    new = "new"
    approved = "approved"


class TestRevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    desc = db.Column(db.String(140), unique=False)  # type: str
    pre_condition = db.Column(db.String(140), unique=False)  # type: str
    post_condition = db.Column(db.String(140), unique=False)  # type: str
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    creation_date = db.Column(db.DateTime, default=db.func.now())
    state = db.Column(db.Enum(TestState), default=TestState.new)

    steps = db.relationship(
        'Step',
        cascade="all"
    )

    # parameters = None  # type: list[str]
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="tests")  # type: User

    def to_map(self):
        return {
            "id": self.id,
            "test_id": self.test_id,
            "title": self.title,
            "desc": self.desc,
            "pre_condition": self.pre_condition,
            "post_condition": self.post_condition,
            "creation_date": self.creation_date,
            "steps": self.steps,
            "state": self.state,
            "author": self.author,
        }

    def update_from_map(self, x):
        self.test_id = x.get("test_id", self.test_id)
        self.title = x.get("title", self.title)
        self.desc = x.get("desc", self.desc)
        self.pre_condition = x.get("pre_condition", self.pre_condition)
        self.post_condition = x.get("post_condition", self.post_condition)
        self.state = x.get("state", self.state)
        steps = x.get("steps", [])
        if steps is None:
            self.steps.clear()
        if steps:
            for s in steps:
                step = Step()
                step.update_from_map(s)
                self.steps.append(step)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=db.func.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    @cached_property
    def last_revision(self):
        return TestRevision.query.filter_by(test_id=self.id).order_by(TestRevision.id.desc()).limit(1).first()

    revisions = db.relationship(
        'TestRevision',
        backref=db.backref('test'),
        cascade="all",
        lazy='dynamic',
    )
    tags = db.relationship(
        'Tag',
        secondary=test_tags,
        cascade="all",
        backref=db.backref('tests', lazy='dynamic'),
    )  # type: list[Tag]

    def to_map(self):
        return {
            "id": self.id,
            "creation_date": self.creation_date,
            "last_revision": self.last_revision,
            "tags": self.tags,
            "project": self.project,
        }
