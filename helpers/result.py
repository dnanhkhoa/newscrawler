#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from enum import Enum


class Result(object):
    class Codes(Enum):
        OK = 0
        URLError = 1
        ParsingError = 2
        Unsupported = 3
        Unknown = 4

    def __init__(self, content=None, status_code=Codes.OK):
        self._status_code = status_code
        self._content = content

    def is_ok(self):
        return self._status_code == Result.Codes.OK

    def get_status_code(self):
        return self._status_code

    def get_content(self):
        return self._content
