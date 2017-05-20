#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.json import JSONEncoder
from data import db
import enum


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, db.Model):
                return obj.to_map()
            elif isinstance(obj, enum.Enum):
                return obj.value
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
