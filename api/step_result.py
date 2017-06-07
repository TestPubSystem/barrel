#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import db
from data import result

from flask import request, Blueprint, jsonify
from flask_jwt import jwt_required

step_result_blueprint = Blueprint("step_result", __name__)


@step_result_blueprint.route("/<int:result_id>", methods=["PUT"])
@jwt_required()
def update_step_result(result_id):
    res = result.StepResult.query.get(result_id)
    if not res:
        return "Step result not found", 404
    data = request.get_json(force=True)
    res.update_from_map(data)
    db.session.commit()
    return jsonify(data=res)
