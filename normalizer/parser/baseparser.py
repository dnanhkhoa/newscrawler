#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class BaseParser(ABC):
    _special_chars = '“”–'
    _normal_chars = '""-'

    _special_chars_removes_map = dict(zip(_special_chars, _normal_chars))
    _special_chars_removes_regex = re.compile('|'.join(_special_chars))

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._domain = None

    @staticmethod
    def remove_special_chars(string):
        return BaseParser._special_chars_removes_regex.sub(lambda m: BaseParser._special_chars_removes_map[m.group(0)],
                                                           string)

    @staticmethod
    def normalize_string(string):
        string = re.sub(r'\\(\S)', r'\g<1>', string)
        return re.sub(r'\s+', ' ', BaseParser.remove_special_chars(string)).strip()

    # Tải nội dung web
    def get_html(self, url, timeout=15):
        try:
            response = requests.get(url=url, timeout=timeout)
            if response.status_code == requests.codes.ok:
                return response.content.decode('UTF-8')
        except Exception as e:
            self._logger.exception(e)
        return None

    def get_page_title(self, html):
        return self.normalize_string(html.title.string)

    def get_meta_keywords(self, html):
        meta_tag = html.find('meta', attrs={'name': 'keywords'})
        if meta_tag is None or not meta_tag.has_attr('content'):
            return None
        keywords = meta_tag.get('content').split(',')
        normalized_keywords = []
        for keyword in keywords:
            normalized_keywords.append(self.normalize_string(keyword))
        return ', '.join(normalized_keywords)

    def get_meta_description(self, html):
        meta_tag = html.find('meta', attrs={'name': 'description'})
        if meta_tag is None or not meta_tag.has_attr('content'):
            return None
        return self.normalize_string(meta_tag.get('content'))

    @abstractmethod
    def get_main_content(self, html, title):
        pass

    @abstractmethod
    def get_content(self, main_content):
        pass

    def get_plain_content(self, content):
        if content is None:
            return None
        return None

    @abstractmethod
    def get_publish_date(self, html, main_content):
        pass

    @abstractmethod
    def get_summary(self, html, main_content):
        pass

    @abstractmethod
    def get_thumbnail(self, html, main_content):
        pass

    @abstractmethod
    def get_author(self, html, main_content):
        pass

    @abstractmethod
    def get_tags(self, html, main_content):
        pass

    def parse(self, url, timeout=15):
        raw_html = self.get_html(url=url, timeout=timeout)
        if raw_html is None:
            raise Exception('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)

        html = BeautifulSoup(raw_html, 'html5lib')

        page_title = self.get_page_title(html=html)
        meta_keywords = self.get_meta_keywords(html=html)
        meta_description = self.get_meta_description(html=html)

        main_content = self.get_main_content(html=html, title=page_title)
        content = self.get_content(main_content=main_content)
        plain_content = self.get_plain_content(content=content)

        publish_date = self.get_publish_date(html=html, main_content=main_content)
        summary = self.get_summary(html=html, main_content=main_content)
        thumbnail = self.get_thumbnail(html=html, main_content=main_content)
        author = self.get_author(html=html, main_content=main_content)
        tags = self.get_tags(html=html, main_content=main_content)

        return {
            'SourcePage': '' if self._domain is None else self._domain,
            'Title': '' if page_title is None else page_title,
            'Url': '' if url is None else url,
            'Author': '' if author is None else author,
            'Thumbnail': '' if thumbnail is None else thumbnail,
            'Tag': '' if tags is None else tags,
            'ShortIntro': '' if summary is None else summary,
            'PublishDate': '' if publish_date is None else publish_date,
            'MetaDescription': '' if meta_description is None else meta_description,
            'MetaKeywords': '' if meta_keywords is None else meta_keywords,
            'CrawledDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Content': '' if content is None else content,
            'Plain_Content': '' if plain_content is None else plain_content
        }
