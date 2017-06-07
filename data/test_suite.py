#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import db
from data.test import Test
from data.tag import Tag
from data.user import User

test_suite_tags = db.Table(
    "test_suite_tags",
    db.Column("tag_id", db.Integer, db.ForeignKey('tag.id')),
    db.Column("test_suite_id", db.Integer, db.ForeignKey('test_suite.id'))
)

test_suite_tests = db.Table(
    "test_suite_tests",
    db.Column("test_id", db.Integer, db.ForeignKey('test.id')),
    db.Column("test_suite_id", db.Integer, db.ForeignKey('test_suite.id'))
)


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    desc = db.Column(db.String(140), unique=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())
    tests = db.relationship(
        'Test',
        secondary=test_suite_tests,
        backref=db.backref('test_suites', lazy='dynamic'),
        cascade="all"
    )  # type: list[Test]
    tags = db.relationship(
        'Tag',
        secondary=test_suite_tags,
        backref=db.backref('test_suites', lazy='dynamic'),
        cascade="all"
    )  # type: list[Tag]
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="test_suites")  # type: User

    def to_map(self):
        return {
            "id": self.id,
            "creation_date": self.creation_date,
            "title": self.title,
            "tests": self.tests,
            "tags": self.tags,
            "desc": self.desc,
            "author": self.author,
        }

    def update_from_map(self, x):
        self.title = x.get("title", self.title)
        self.desc = x.get("desc", self.desc)
