#!/usr/bin/python
# -*- coding: utf8 -*-
import re

from normalizer.parser.baseparser import BaseParser


class LaoDongXaHoiNetParser(BaseParser):
    def __init__(self):
        super().__init__()
        self._domain = 'laodongxahoi.net'

    def get_tags(self, html):
        div_tag = html.find('div', class_='tag_detail')
        if div_tag is None:
            return None
        tags = []
        a_tags = div_tag.find_all('a')
        for tag in a_tags:
            tags.append(self.normalize_string(re.sub(r'\\(\S)', r'\g<1>', tag.get_text())))
        return ', '.join(tags)

    def get_summary(self, html):
        pass

    def get_content(self, html):
        pass

    def get_thumbnail(self, html):
        pass

    def get_publish_date(self, html):
        pass

    def get_author(self, html):
        pass
