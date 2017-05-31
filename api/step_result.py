#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data import db
from data import result

from flask import request, Blueprint, jsonify

step_result_blueprint = Blueprint("step_result", __name__)


@step_result_blueprint.route("/<int:result_id>", methods=["PUT"])
def update_step_result(result_id):
    res = result.StepResult.query.get(result_id)
    if not res:
        return "Step result not found", 404
    data = request.get_json(force=True)
    res.update_from_map(data)
    return jsonify(data=res)
