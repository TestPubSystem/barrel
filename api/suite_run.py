#!/usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify

from data import test
from data import db
from data import tag
from data import result
from data import suite_run
from data import test_suite

suite_run_blueprint = Blueprint("suite_run", __name__)


@suite_run_blueprint.route("/suite_runs/")
def get_suite_runs():
    runs = suite_run.SuiteRun.query.all()
    return jsonify(data=runs)


@suite_run_blueprint.route("/suite_runs/", methods=["POST"])
def create_suite_run():
    data = request.get_json(Force=True)
    suite = test_suite.TestSuite.query(data["test_suite_id"])
    return
