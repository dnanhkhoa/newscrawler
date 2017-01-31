#!/usr/bin/python
# -*- coding: utf8 -*-
import regex

from crawler.parser import BaseParser
from helpers import create_parser_from_files


class Crawler(object):
    _domain_regex = regex.compile(r'^https?://(?:www\.)?(\w+(?:\.\w+)+)', regex.IGNORECASE)

    def __init__(self):
        self.parser = create_parser_from_files('crawler/parser/subclasses', BaseParser)

    def crawl(self, url, date=None, timeout=15):
        matcher = self._domain_regex.search(url)
        if matcher is None:
            raise Exception('URL không hợp lệ: %s' % url)
        domain = matcher.group(1)
        if domain not in self.parser:
            raise Exception('Tên miền %s chưa được hỗ trợ.' % domain)
        return self.parser[domain].parse(url=url, date=date, timeout=timeout)
