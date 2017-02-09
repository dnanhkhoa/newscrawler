#!/usr/bin/python
# -*- coding: utf8 -*-
from normalizer.parser import *


class LaoDongXaHoiNetParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._source_page = 'Lao Động Xã Hội'
        self._domain = 'laodongxahoi.net'

        # Thay đổi các hàm trong vars để thay đổi các tham số của hàm cha
        # Publish date
        self._vars['get_time_tag_func'] = lambda x: x.find('div', class_='time_detail_news')
        self._vars['get_datetime_func'] = lambda x: datetime.strptime(x, '%I:%M %p %d/%m/%Y')

        # Main content
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', id='cotent_detail')

    def _get_author(self, html):
        pass

    def _handle_video(self, html, timeout=15):
        return html
