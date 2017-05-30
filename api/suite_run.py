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

suite_run_blueprint = Blueprint("suite_run", __name__)


@suite_run_blueprint.route("/suite_runs/")
def suite_runs():
    return
