#!/usr/bin/python
# -*- coding: utf8 -*-
from normalizer.parser import *


class GiaoDucThoiDaiVnParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._source_page = 'Giáo Dục Thời Đại'
        self._domain = 'giaoducthoidai.vn'
        self._full_domain = 'http://giaoducthoidai.vn'

        # Thay đổi các hàm trong vars để thay đổi các tham số của hàm cha
        # Publish date
        def get_time_tag_func(html):
            div_tag = html.find('div', class_='toolbar')
            if div_tag is None:
                return None
            span_tag = div_tag.find('span', class_='time')
            if span_tag is None:
                return None
            return span_tag

        self._vars['get_time_tag_func'] = get_time_tag_func

        def get_datetime_func(string):
            string = string.split(',')[1]
            parts = string.strip().split(' ')[:-1]
            return datetime.strptime(' '.join(parts), '%d/%m/%Y %H:%M')

        self._vars['get_datetime_func'] = get_datetime_func

        # Main content
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', id='articlecontent')

    def _handle_video(self, html, timeout=15):
        return html
