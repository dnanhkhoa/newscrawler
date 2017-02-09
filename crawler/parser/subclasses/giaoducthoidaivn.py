#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class GiaoDucThoiDaiVnParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._domain = 'giaoducthoidai.vn'
        self._full_domain = 'http://giaoducthoidai.vn'

        # Active tag
        def get_active_tag_func(html):
            span_tag = html.find('span', id='ctl00_mainContent_ContentList1_pager')
            li_tags = span_tag.find_all('li')
            for li_tag in li_tags:
                li_tag.unwrap()
            span_tag.ul.unwrap()

            a_tag = span_tag.find(lambda x: x.name == 'a' and len(x.attrs) == 0)
            return None if a_tag is None else a_tag

        self._vars['get_active_tag_func'] = get_active_tag_func

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

        # Post urls
        def get_post_urls_func(html):
            urls = []

            # Child posts
            posts = html.find_all('article', class_='story')
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

    def _pre_process(self, html):
        section_tag = html.find('section', class_='browsing-focus')
        if section_tag is None:
            return None
        section_tag = section_tag.find('div', class_='pull-left')
        if section_tag is None:
            return None
        return super()._pre_process(section_tag)
