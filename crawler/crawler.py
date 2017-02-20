#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import BaseParser
from helpers import *


# Lớp đảm nhận nhiệm load các parsers lên trước
class Crawler(object):
    def __init__(self):
        self._domain_regex = [regex.compile(r'^https?://(?:www\.)?(\w+(?:\.\w+)+)', regex.IGNORECASE)]
        self._parser = create_parser_from_files('crawler/parser/subclasses', BaseParser)

        # Thêm các domain_regex từ các parsers
        for k in self._parser:
            patterns = self._parser[k].get_domain_regex()
            if isinstance(patterns, list):
                self._domain_regex.extend(patterns)

        # Lọc trùng
        self._domain_regex = list(set(self._domain_regex))

    def crawl(self, url, from_date=None, to_date=None, timeout=15):
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
            content=self._parser[domain].parse(url=url, from_date=from_date, to_date=to_date, timeout=timeout))
