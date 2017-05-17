#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import enum


@enum.unique
class StepType(enum.Enum):
    step = "step"
    expected_result = "expected_result"


class Step:
    type = None  # type: StepType
    id = None
    text = None  # type: str
    attachments = None  # type: list
    order_number = None


class TestRevision:
    id = None
    title = None
    steps = None  # type: list[Step]
    desc = None  # type: str
    pre_condition = None  # type: str
    post_condition = None  # type: str
    parameters = None  # type: list[str]
    test_id = None
    author_id = None
    creation_date = None  # type: datetime.datetime


class Test:
    id = None
    last_revision = None  # type: TestRevision
    tags = None  # type: list[str]
    author_id = None
    creation_date = None  # type: datetime.datetime


class TestSuite:
    id = None
    title = None  # type: str
    tests = None  # type: list[Test]
    tags = None  # type: list[str]
    author_id = None
    creation_date = None  # type: datetime.datetime
