#!/usr/bin/python
# -*- coding: utf8 -*-
from normalizer.parser import *


class PhuNuTodayVnParser(SubBaseParser):
    _video_url_regex = regex.compile(r'file\s*:\s*"([^"]+)"', regex.IGNORECASE)
    _trash_classes_regex = regex.compile(r'list_suggest_link|list_suggest_desk|adv', regex.IGNORECASE)

    def __init__(self):
        super().__init__()

        self._source_page = 'Phụ Nữ Today'
        self._domain = 'phunutoday.vn'

        # Thay đổi các hàm tron vars để thay đổi các tham số của hàm cha
        # Publish date
        self._vars['get_time_tag_func'] = lambda x: x.find('time', class_='fl')
        self._vars['get_datetime_func'] = lambda x: datetime.strptime(regex.sub(r',[^\d]+', ' ', x), '%H:%M %d/%m/%Y')

        # Main content
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', id='content_detail')

    def _get_summary(self, html):
        return self._get_meta_description(html=html)

    def _get_tags(self, html):
        return self._get_meta_keywords(html=html)

    def _get_author(self, html):
        div_tag = html.find_next('div', class_='tags')
        if div_tag is None:
            return None
        div_tag = div_tag.find_next_sibling(lambda x: x.name == 'div' and x.p is not None)
        if div_tag is None:
            return None
        return normalize_string(div_tag.p.text)

    def _get_direct_video(self, url, timeout=15):
        if self._domain not in url:
            return None

        raw_html = get_html(url=url, timeout=timeout)
        if raw_html is None:
            return None

        matcher = self._video_url_regex.search(raw_html)
        return None if matcher is None else matcher.group(1)

    def _handle_video(self, html, timeout=15):
        video_tags = html.find_all('iframe', attrs={'class': 'exp_video', 'src': True})
        for video_tag in video_tags:
            video_url = video_tag.get('src')
            video_url = self._get_direct_video(url=video_url, timeout=timeout)
            if video_url is None:
                video_tag.decompose()  # Xóa bỏ thẻ nếu không thể lấy được URL trực tiếp của video
            else:
                video_tag.replace_with(create_video_tag(src=video_url))
        return html

    def _pre_process_before_normalizing(self, html):
        # Remove ads
        trash_items = html.find_all(class_=self._trash_classes_regex)
        for trash_item in trash_items:
            trash_item.decompose()
        return super()._pre_process_before_normalizing(html)
