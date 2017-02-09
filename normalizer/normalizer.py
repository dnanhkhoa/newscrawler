#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from helpers import *
from normalizer.parser import BaseParser


class Normalizer(object):
    def __init__(self):
        self._domain_regex = [regex.compile(r'^https?://(?:www\.)?(\w+(?:\.\w+)+)', regex.IGNORECASE)]
        self._parser = create_parser_from_files('normalizer/parser/subclasses', BaseParser)

        # Thêm các domain_regex từ các parsers
        for k in self._parser:
            patterns = self._parser[k].get_domain_regex()
            if isinstance(patterns, list):
                self._domain_regex.extend(patterns)

        # Lọc trùng
        self._domain_regex = list(set(self._domain_regex))

    def normalize(self, url, timeout=15):
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
            return None

        return self._parser[domain].parse(url=url, timeout=timeout)
