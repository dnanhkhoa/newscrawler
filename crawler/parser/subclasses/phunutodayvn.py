#!/usr/bin/python
# -*- coding: utf8 -*-
from crawler import *


class PhuNuTodayVnParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.domain = 'phunutoday.vn'

    def get_post_date(self, url):
        pass

    def get_urls(self, html, date):
        urls = []


        return urls

    def get_category_urls(self, html):
        return None
