#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import enum


@enum.unique
class Role(enum.Enum):
    manager = "manager"
    tester = "tester"
    test_designer = "test_designer"


class UserAuth:
    user_id = None
    salt = None
    hash = None


class User:
    roles = None  # type: list[Role]
    login = None
    name = None
    email = None
    avatar = None
    registration_date = None  # type: datetime.datetime
    blocked = False  # type: bool
    confirmed = False  # type: bool
