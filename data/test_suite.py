#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import db
from data.test import Test
from data.tag import Tag

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
    creation_date = db.Column(db.DateTime, default=db.func.now())
    tests = db.relationship(
        'Test',
        secondary=test_suite_tests,
        backref=db.backref('suites', lazy='dynamic'),
        cascade="all"
    )
    tags = db.relationship(
        'Tag',
        secondary=test_suite_tags,
        cascade="all"
    )

    def to_map(self):
        return {
            "id": self.id,
            "creation_date": self.creation_date,
            "title": self.title,
            "tests": self.tests,
            "tags": self.tags,
        }

    @classmethod
    def from_map(cls, x):
        self = TestSuite()
        self.update_from_map(x)
        return self

    def update_from_map(self, x):
        self.title = x.get("title")

    # author_id = None
