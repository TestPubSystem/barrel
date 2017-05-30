#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify

from data.test import TestRevision, Test
from data import db
from data import test_run

test_run_blueprint = Blueprint("test_run", __name__)


@test_run_blueprint.route("/")
def get_test_runs():
    runs = test_run.TestRun.query.all()
    return jsonify(data=runs)


@test_run_blueprint.route("/<int:run_id>")
def get_suite_run(run_id):
    runs = test_run.TestRun.query.get(run_id)
    return jsonify(data=runs)


@test_run_blueprint.route("/", methods=["POST"])
def create_suite_run():
    data = request.get_json(force=True)
    run = None  # type: test_run.TestRun
    rev_id = data.get("test_revision_id")
    if rev_id:
        run = test_run.create_from_test_revision(TestRevision.query.get(rev_id))
    else:
        run = test_run.create_from_test(Test.query.get(data["test_id"]))
    db.session.add(run)
    db.session.commit()
    return jsonify(data=run)
