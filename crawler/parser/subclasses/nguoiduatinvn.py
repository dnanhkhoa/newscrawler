#!/usr/bin/python
# -*- coding: utf8 -*-
from normalizer.parser import *


class NguoiDuaTinVnParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._source_page = 'Người Đưa Tin'
        self._domain = 'nguoiduatin.vn'

        # Thay đổi các hàm tron vars để thay đổi các tham số của hàm cha
        # Publish date
        self._vars['get_time_tag_func'] = lambda x: x.find('div', class_='right metadata')
        self._vars['get_datetime_func'] = lambda x: datetime.strptime(x, '%d.%m.%Y | %H:%M %p')

        # Main content
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', id='main-detail')

    def _get_author(self, html):
        pass

    def _handle_video(self, html, timeout=15):
        return html
