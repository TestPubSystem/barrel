#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt import jwt_required, current_identity

from data import db
from data import suite_run
from data.test_suite import TestSuite
from data.user import User

suite_run_blueprint = Blueprint("suite_run", __name__)


@suite_run_blueprint.route("/")
@jwt_required()
def get_suite_runs():
    runs = suite_run.SuiteRun.query.all()
    return jsonify(data=runs)


@suite_run_blueprint.route("/<int:run_id>")
@jwt_required()
def get_suite_run(run_id):
    runs = suite_run.SuiteRun.query.get(run_id)
    if not runs:
        return "Suite run not found", 404
    return jsonify(data=runs)


@suite_run_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_suite_run():
    data = request.get_json(force=True)
    suite = TestSuite.query.get(data["test_suite_id"])
    assignee_id = data.get("assignee", {}).get("id")
    assignee = User.query.get(assignee_id) if assignee_id else None
    run = suite_run.create_from_test_suite(suite, current_identity, assignee)
    db.session.add(run)
    db.session.commit()
    return jsonify(data=run)


@suite_run_blueprint.route("/<int:run_id>", methods=["PATCH"])
@jwt_required()
def update_suite_run(run_id):
    run = suite_run.SuiteRun.query.get(run_id)  # type: suite_run.SuiteRun
    if not run:
        return "Suite run not found", 404
    data = request.get_json(force=True)
    if "assignee" in data:
        assignee_id = data["assignee"].get("id")
        assignee = User.query.get(assignee_id) if assignee_id else None
        run.assignee = assignee
    db.session.commit()
    return jsonify(data=run)
