#!/usr/bin/python
# -*- coding: utf8 -*-
import logging

import regex

from normalizer.parser import BaseParser
from utils import create_parser_from_files


class Normalizer(object):
    _domain_regex = regex.compile(r'^https?://(?:www\.)?(\w+(?:\.\w+)+)', regex.IGNORECASE)

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.parser = create_parser_from_files('normalizer/parser/subclasses', BaseParser)

    def normalize(self, url, timeout=15):
        result = self._domain_regex.search(url)
        if result is None:
            raise Exception('URL không hợp lệ: %s' % url)
        domain = result.group(1)
        if domain not in self.parser:
            raise Exception('Không có parser nào hỗ trợ URL: %s' % url)
        return self.parser[domain].parse(url=url, timeout=timeout)
