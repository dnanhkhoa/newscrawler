#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class PhuNuTodayVnParser(SubBaseParser):
    def __init__(self):
        super().__init__()

        self._domain = 'phunutoday.vn'
        self._full_domain = 'http://www.phunutoday.vn'

        # Child category urls
        self._vars['get_child_category_section_func'] = lambda x: x.find('ul', class_='cat_child')

        # Active tag
        def get_active_tag_func(html):
            tags = html.select('div.paging > a.active')
            return tags[0] if len(tags) > 0 else None

        self._vars['get_active_tag_func'] = get_active_tag_func

        # Publish date
        self._vars['get_time_tag_func'] = lambda x: x.find('time', class_='fl')
        self._vars['get_datetime_func'] = lambda x: datetime.strptime(regex.sub(r',[^\d]+', ' ', x), '%H:%M %d/%m/%Y')

        # Post urls
        def get_post_urls_func(html):
            urls = []

            # Thumbnail posts
            div_tag = html.find('article', class_='n_lock')
            if div_tag is not None:
                a_tag = div_tag.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            # Other posts
            ul_tag = html.find('ul', class_='n_other')
            if ul_tag is not None:
                posts = ul_tag.find_all('article')
                for post in posts:
                    a_tag = post.find('a', attrs={'href': True})
                    if a_tag is not None:
                        urls.append(a_tag.get('href'))

            # Child posts
            posts = html.find_all('div', class_='news_info')
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func
