#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt import jwt_required, current_identity

from data import project
from data import db

project_blueprint = Blueprint("project", __name__)


@project_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_projects(offset=0, limit=20):
    res = project.Project.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@project_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_project():
    res = project.Project()
    data = request.get_json(force=True)
    res.update_from_map(data)
    res.author = current_identity
    db.session.add(res)
    db.session.commit()
    return jsonify(data=res)


@project_blueprint.route("/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    proj = project.Project.query.get(project_id)  # type: project.Project
    if not proj:
        return "Project not found", 404
    return jsonify(data=proj)


@project_blueprint.route("/<int:project_id>", methods=["PATCH"])
@jwt_required()
def patch_project(project_id):
    proj = project.Project.query.get(project_id)  # type: project.Project
    if not proj:
        return "Project not found", 404
    data = request.get_json(force=True)
    proj.update_from_map(data)
    db.session.commit()
    return jsonify(data=proj)


@project_blueprint.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    proj = project.Project.query.get(project_id)  # type: project.Project
    if not proj:
        return "Project not found", 404
    db.session.delete(proj)
    db.session.commit()
    return jsonify()


@project_blueprint.route("/<int:project_id>/tests/", methods=["GET"])
@jwt_required()
def get_project_tests(project_id):
    proj = project.Project.query.get(project_id)  # type: project.Project
    if not proj:
        return "Project not found", 404
    return jsonify(data=proj.tests)


@project_blueprint.route("/<int:project_id>/testsuites/", methods=["GET"])
@jwt_required()
def get_project_suites(project_id):
    proj = project.Project.query.get(project_id)  # type: project.Project
    if not proj:
        return "Project not found", 404
    return jsonify(data=proj.test_suites)
