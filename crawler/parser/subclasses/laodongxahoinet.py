#!/usr/bin/python
# -*- coding: utf8 -*-
from crawler.parser import *


class LaoDongXaHoiNetParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._domain = 'laodongxahoi.net'

        # Child category urls
        self._vars['get_child_category_section_func'] = lambda x: x.find('div', class_='bread_right')
