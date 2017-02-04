#!/usr/bin/python
# -*- coding: utf8 -*-
from abc import abstractmethod
from copy import copy

import bleach

from helpers import *
from normalizer.parser import BaseParser


class SubBaseParser(BaseParser):
    def __init__(self):
        super().__init__()

    def _get_post_title(self, html):
        get_title_tag_func = self._vars.get('get_title_tag_func')
        title_tag = html.title if get_title_tag_func is None else get_title_tag_func(html)
        if title_tag is None:
            return None
        return normalize_string(title_tag.text) if is_valid_string(title_tag.text) else None

    def _get_meta_keywords(self, html):
        meta_tag = html.find('meta', attrs={'name': 'keywords', 'content': True})
        if meta_tag is None:
            return None

        keywords = meta_tag.get('content').split(',')
        normalized_keywords = []
        for keyword in keywords:
            if is_valid_string(keyword):
                normalized_keywords.append(normalize_string(keyword))
        return ', '.join(normalized_keywords)

    def _get_meta_description(self, html):
        meta_tag = html.find('meta', attrs={'name': 'description', 'content': True})
        if meta_tag is None:
            return None

        content = meta_tag.get('content')
        return normalize_string(content) if is_valid_string(content) else None

    def _get_summary(self, html):
        get_summary_tag_func = self._vars.get('get_summary_tag_func')
        if get_summary_tag_func is None:
            return None

        summary_tag = get_summary_tag_func(html)
        if summary_tag is None:
            return None

        content = summary_tag.text
        return normalize_string(content) if is_valid_string(content) else None

    def _get_tags(self, html):
        get_tags_tag_func = self._vars.get('get_tags_tag_func')
        if get_tags_tag_func is None:
            return None

        tags_tag = get_tags_tag_func(html)
        if tags_tag is None:
            return None

        normalized_keywords = []
        for a_tag in tags_tag.find_all('a'):
            keyword = a_tag.text
            if is_valid_string(keyword):
                normalized_keywords.append(normalize_string(keyword))
        return ', '.join(normalized_keywords)

    def _get_publish_date(self, html):
        get_time_tag_func = self._vars.get('get_time_tag_func')
        get_datetime_func = self._vars.get('get_datetime_func')
        if get_time_tag_func is None or get_datetime_func is None:
            return None

        time_tag = get_time_tag_func(html)
        if time_tag is None:
            return None

        return get_datetime_func(normalize_string(time_tag.text))

    @abstractmethod
    def _handle_video(self, html, timeout=15):
        pass

    def _handle_image(self, html, title=None):
        # Dò ảnh
        # Dò caption
        # Xóa parent chứ ảnh và caption
        return html

    def _remove_trash_before_normalizing(self, html):
        return html

    def _remove_trash_after_normalizing(self, html):
        return html

    def _normalize_content(self, html, title=None, timeout=15):
        get_main_content_tag_func = self._vars.get('get_main_content_tag_func')
        if get_main_content_tag_func is None:
            return None

        main_content_tag = get_main_content_tag_func(html)
        if main_content_tag is None:
            return None

        # Lưu thẻ cha lại để khôi phục sau khi xử lí thẻ con
        content_tag = copy(main_content_tag)

        # Xóa rác
        content_tag = self._remove_trash_before_normalizing(html=content_tag)

        # Xử lí thẻ video
        content_tag = self._handle_video(html=content_tag, timeout=timeout)

        # Chuẩn hóa
        content_tag.name = 'main'

        attrs = {
            'video': ['width', 'height'],
            'source': ['src', 'type'],
            'img': ['src', 'alt'],
            'div': ['align', 'style'],
            'p': ['align', 'style']
        }
        styles = ['text-align']
        content_tag = bleach.clean(content_tag,
                                   tags=['main', 'div', 'p', 'br', 'video', 'source', 'img', 'caption', 'center',
                                         'strong', 'b', 'em', 'i'], attributes=attrs, styles=styles, strip=True,
                                   strip_comments=True)

        content_tag = get_soup(content_tag).main

        block_tags = content_tag.find_all(['div', 'p', 'video', 'img', 'caption', 'center'])
        for block_tag in block_tags:
            block_tag.insert_before(create_html_tag('br', is_self_closing=True))
            block_tag.insert_after(create_html_tag('br', is_self_closing=True))

        # Hỗ trợ dự đoán caption của image và tác giả bài viết
        tags = content_tag.find_all(['div', 'p', 'video', 'img', 'caption', 'center', 'strong', 'b', 'em', 'i'])
        for tag in tags:
            if tag.name in ['div', 'p']:
                pass
            elif tag.name in ['center', 'strong', 'b', 'em', 'i']:
                pass
            elif tag.name in ['caption']:
                pass

        for k in content_tag.contents:
            print('--------------')
            print(k)

        # print(content_tag.prettify())

        # Xử lí thẻ image
        content_tag = self._handle_image(html=content_tag, title=title)

        # Chuẩn hóa kết quả
        content_tag = self._remove_trash_after_normalizing(html=content_tag)

        # Khôi phục sau khi xử lí xong
        main_content_tag.replace_with(content_tag)

        return main_content_tag

    def _get_author(self, html):
        return html

    def _get_thumbnail(self, html):
        img_tag = html.find('img', attrs={'src': True})
        if img_tag is None:
            return None
        return img_tag.get('src')

    def _get_content(self, html):
        return ''

    def _get_plain(self, html):
        return ''

    def _parse(self, url, html, timeout=15):
        post_title = self._get_post_title(html=html)
        meta_keywords = self._get_meta_keywords(html=html)
        meta_description = self._get_meta_description(html=html)

        publish_date = self._get_publish_date(html=html)
        tags = self._get_tags(html=html)
        summary = self._get_summary(html=html)

        normalized_content = self._normalize_content(html=html, title=remove_special_chars(post_title), timeout=timeout)
        author = self._get_author(html=normalized_content)
        thumbnail = self._get_thumbnail(html=normalized_content)
        content = self._get_content(html=normalized_content)
        plain = self._get_plain(html=normalized_content)

        return self._build_json(url=url, title=post_title, meta_keywords=meta_keywords,
                                meta_description=meta_description, publish_date=publish_date, author=author, tags=tags,
                                thumbnail=thumbnail, summary=summary, content=content, plain=plain)
