#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt import jwt_required, current_identity

from data.test import TestRevision, Test
from data import db
from data import test_run
from data.user import User

test_run_blueprint = Blueprint("test_run", __name__)


@test_run_blueprint.route("/")
@jwt_required()
def get_test_runs():
    runs = test_run.TestRun.query.all()
    return jsonify(data=runs)


@test_run_blueprint.route("/<int:run_id>")
@jwt_required()
def get_suite_run(run_id):
    runs = test_run.TestRun.query.get(run_id)
    if not runs:
        return "Test run not found", 404
    return jsonify(data=runs)


@test_run_blueprint.route("/<int:run_id>", methods=["PATCH"])
@jwt_required()
def patch_suite_run(run_id):
    runs = test_run.TestRun.query.get(run_id)  # type: test_run.TestRun
    if not runs:
        return "Test run not found", 404
    data = request.get_json(force=True)
    runs.update_from_map(data)
    return jsonify(data=runs)


@test_run_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_suite_run():
    data = request.get_json(force=True)
    run = None  # type: test_run.TestRun
    rev_id = data.get("test_revision_id")
    assignee_id = data.get("assignee", {}).get("id")
    assignee = User.query.get(assignee_id) if assignee_id else None
    if rev_id:
        run = test_run.create_from_test_revision(TestRevision.query.get(rev_id), current_identity, assignee)
    else:
        run = test_run.create_from_test(Test.query.get(data["test_id"]), current_identity, assignee)
    db.session.add(run)
    db.session.commit()
    return jsonify(data=run)
