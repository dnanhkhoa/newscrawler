#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from checker.basecheckers import BaseChecker
from helpers import *


# Lớp đảm nhận nhiệm load các checkers lên trước
class Checker(object):
    def __init__(self):
        self._domain_regex = [regex.compile(r'^https?://(?:www\.)?(\w+(?:\.\w+)+)', regex.IGNORECASE)]
        self._parser = create_parser_from_files('checker/basecheckers/subclasses', BaseChecker)

        # Thêm các domain_regex từ các checkers
        for k in self._parser:
            patterns = self._parser[k].get_domain_regex()
            if isinstance(patterns, list):
                self._domain_regex.extend(patterns)

        # Lọc trùng
        self._domain_regex = list(set(self._domain_regex))

    def check(self, url, timeout=15, attempts=3):
        domain = None
        for pattern in self._domain_regex:
            matcher = pattern.search(url)
            if matcher is not None:
                matcher = matcher.group(1)
                if matcher in self._parser:
                    domain = matcher
                    break

        if domain is None:
            log('Tên miền %s chưa được hỗ trợ.' % domain)
            return Result(status_code=Result.Codes.Unsupported)

        return Result(
            content=self._parser[domain].check(url=url, timeout=timeout, attempts=attempts))
