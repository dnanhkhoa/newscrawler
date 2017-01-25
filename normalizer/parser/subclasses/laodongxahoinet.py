#!/usr/bin/python
# -*- coding: utf8 -*-
import bleach

from normalizer import *


class LaoDongXaHoiNetParser(BaseParser):
    def __init__(self):
        super().__init__()
        self._domain = 'laodongxahoi.net'

    def get_author(self, html, main_content):
        pass

    def get_tags(self, html, main_content):
        div_tag = html.find('div', class_='tag_detail')
        if div_tag is None:
            return None
        tags = []
        a_tags = div_tag.find_all('a')
        for tag in a_tags:
            tags.append(self.normalize_string(tag.text))
        return ', '.join(tags)

    def get_thumbnail(self, html, main_content):
        img_tag = main_content.find('img')
        if img_tag is None:
            return None
        return img_tag.get('src')

    def get_content(self, main_content):
        return str(main_content)

    def get_summary(self, html, main_content):
        div_tag = html.find('div', class_='sapo_detail')
        if div_tag is None:
            return None
        return self.normalize_string(div_tag.text)

    def get_publish_date(self, html, main_content):
        div_tag = html.find('div', class_='time_detail_news')
        if div_tag is None:
            return None
        time_string = div_tag.text.strip()
        return datetime.strptime(time_string, '%I:%M %p %d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')

    def get_main_content(self, html, title):
        div_tag = html.find('div', id='cotent_detail')
        if div_tag is None:
            return None
        attrs = {'p': ['align', 'style'],
                 'div': ['style'],
                 'img': ['src', 'alt']}
        styles = ['text-align']
        print(div_tag)
        print(
            bleach.clean(div_tag, tags=['div', 'p', 'img', 'em', 'strong'], attributes=attrs, styles=styles, strip=True,
                         strip_comments=True))
        return div_tag
