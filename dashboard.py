#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum


class ReportType(enum.Enum):
    suite_chart = "suite"
    suite_trend = "suite_trend"
    suite_run_chart = "suite_run_chart"
    suite_run_trend = "suite_run_trend"
    last_runs_list = "last_runs_list"


class Report:
    type = None


class DashBoard:
    owner_id = None
    reports = None  # type: list[Report]
