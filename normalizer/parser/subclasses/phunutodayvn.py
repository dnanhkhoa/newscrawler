#!/usr/bin/python
# -*- coding: utf8 -*-
import dateparser

from normalizer import *


class PhuNuTodayVnParser(BaseParser):
    def __init__(self):
        super().__init__()
        self._domain = 'phunutoday.vn'

    def handle_video_tag(self, html):
        return html

    def handle_image_tag(self, html):
        return html

    def get_main_content(self, html, title):
        div_tag = html.find('div', id='content_detail')
        if div_tag is None:
            return None

        trash_items = div_tag.find_all(class_=regex.compile(r'list_suggest_link|list_suggest_desk|adv'))
        for trash_item in trash_items:
            trash_item.decompose()

        # Handle video
        video_tags = div_tag.find_all('iframe', class_='exp_video')
        for video_tag in video_tags:
            pass
        return div_tag

    def get_tags(self, html, main_content):
        return self.get_meta_keywords(html=html)

    def get_summary(self, html, main_content):
        return self.get_meta_description(html=html)

    def get_content(self, main_content):
        pass

    def get_author(self, html, main_content):
        div_tag = html.find('div', class_='tags')
        if div_tag is None:
            return None
        div_tag = div_tag.find_next('div')
        if div_tag is None:
            return None
        return self.normalize_string(div_tag.p.text)

    def get_thumbnail(self, html, main_content):
        img_tag = main_content.find('img')
        if img_tag is None:
            return None
        return img_tag.get('src')

    def get_publish_date(self, html, main_content):
        time_tag = html.find('time', class_='fl')
        if time_tag is None:
            return None
        publish_date = dateparser.parse(time_tag.span.text.strip(), settings={'DATE_ORDER': 'DMY'}, languages=['vi'])
        return publish_date.strftime('%Y-%m-%d %H:%M:%S')
