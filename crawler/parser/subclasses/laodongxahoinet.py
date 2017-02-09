#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class LaoDongXaHoiNetParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._domain = 'laodongxahoi.net'
        self._full_domain = 'http://laodongxahoi.net'

        # Child category urls
        self._vars['get_child_category_section_func'] = lambda x: x.find('div', class_='bread_right')

        # Active tag
        def get_active_tag_func(html):
            tags = html.select('div.paging > a.active')
            return tags[0] if len(tags) > 0 else None

        self._vars['get_active_tag_func'] = get_active_tag_func

        # Publish date
        self._vars['get_time_tag_func'] = lambda x: x.find('div', class_='time_detail_news')
        self._vars['get_datetime_func'] = lambda x: datetime.strptime(x, '%I:%M %p %d/%m/%Y')

        # Post urls
        def get_post_urls_func(html):
            urls = []

            # Thumbnail posts
            div_tags = html.find_all('div', class_=lambda x: x in ['col420', 'col240'])
            for div_tag in div_tags:
                a_tag = div_tag.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            # Child posts
            posts = html.find_all('div', class_='info_cate')
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

    def _pre_process(self, html):
        html = html.find('div', class_='col660')
        if html is None:
            return None
        return super()._pre_process(html)
