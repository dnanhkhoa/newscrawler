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

        # Title
        # self._vars['get_title_tag_func'] = lambda x: x.find('h1', class_='cms-title')

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
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', id='abody')

    def _handle_video(self, html, timeout=15):
        video_tags = html.find_all('div', class_='cms-video')
        for video_tag in video_tags:
            video_url = video_tag.get('data-video-src')
            if video_url is None:
                video_tag.decompose()  # Xóa bỏ thẻ nếu không thể lấy được URL trực tiếp của video
            else:
                video_tag.replace_with(create_video_tag(src=video_url))
        return html

    def _get_tags(self, html):
        return super()._get_meta_keywords(html)

    def _get_author(self, html):
        author = html.find('p', class_='author')
        return None if author is None else author.text
