#!/usr/bin/env python
# -*- coding: utf-8 -*-

import test
import datetime
import enum


@enum.unique
class Status(enum.Enum):
    success = "success"
    partial = "partial"
    failed = "failed"
    blocked = "blocked"
    none = None


class StepResult:
    step_id = None
    id = None
    date = None  # type: datetime.datetime
    status = None  # type: Status
    step = None  # type: test.Step
    comment = None  # type: str
    attachments = None


class TestResult:
    id = None
    revision_id = None
    step_statuses = None  # type: StepResult
    status = None  # type: Status
    comment = None  # type: str
    attachments = None
    author_id = None
    finish_date = None  # type: datetime.datetime


class SuiteRun:
    id = None
    suite_id = None
    tests = None  # type: list[test.Test]
    results = None  # type: list[TestResult]
    author_id = None
    start_date = None  # type: datetime.datetime
    finish_date = None  # type: datetime.datetime
