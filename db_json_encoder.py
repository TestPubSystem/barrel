#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.json import JSONEncoder
import enum
import datetime

from data import db


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, db.Model):
                return obj.to_map()
            elif isinstance(obj, enum.Enum):
                return obj.value
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
