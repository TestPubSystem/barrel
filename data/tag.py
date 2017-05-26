#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    color = db.Column(db.Integer)

    def to_map(self):
        return {
            "id": self.id,
            "title": self.title,
            "color": self.color,
        }

    @classmethod
    def from_map(cls, data):
        t = Tag()
        t.update_from_map(data)
        return t

    def update_from_map(self, data):
        self.color = data.get("color", self.color)
        self.title = data.get("title", self.title)
