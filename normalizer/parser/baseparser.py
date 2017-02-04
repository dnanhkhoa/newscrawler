#!/usr/bin/python
# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from urllib.parse import urljoin

from helpers import *


class BaseParser(ABC):
    def __init__(self):
        self._source_page = None
        self._domain = None
        self._vars = {}

    # Trả về URL tuyệt đối
    def _get_absolute_url(self, url):
        return urljoin(self._domain, url)

    # Trả về image url hợp lệ
    def _get_valid_image_url(self, url):
        image_url = self._get_absolute_url(url=url)
        cleaned_image_url = clean_url_query(url=image_url)
        if is_valid_image_url(cleaned_image_url):
            image_url = cleaned_image_url
        return image_url

    # Trả về kết quả có cấu trúc theo yêu cầu
    def _build_json(self, url=None, title=None, meta_keywords=None, meta_description=None, publish_date=None,
                    author=None, tags=None, thumbnail=None, summary=None, content=None, plain=None):
        return {
            'SourcePage': '' if self._source_page is None else self._source_page,
            'Title': '' if title is None else title,
            'Url': '' if url is None else url,
            'Author': '' if author is None else author,
            'Thumbnail': '' if thumbnail is None else thumbnail,
            'Tag': '' if tags is None else tags,
            'ShortIntro': '' if summary is None else summary,
            'PublishDate': '' if publish_date is None else format_datetime(publish_date),
            'MetaDescription': '' if meta_description is None else meta_description,
            'MetaKeywords': '' if meta_keywords is None else meta_keywords,
            'CrawledDate': format_datetime(datetime.now()),
            'Content': '' if content is None else content,
            'Plain_Content': '' if plain is None else plain
        }

    # Trả về tiêu đề của bài viết
    @abstractmethod
    def _get_post_title(self, html):
        pass

    # Trả về chuỗi keywords đã được chuẩn hóa từ thẻ meta
    @abstractmethod
    def _get_meta_keywords(self, html):
        pass

    # Trả về chuỗi description đã được chuẩn hóa từ thẻ meta
    @abstractmethod
    def _get_meta_description(self, html):
        pass

    # Trả về ngày đăng của bài viết ở dạng chuỗi
    @abstractmethod
    def _get_publish_date(self, html):
        pass

    # Trả về phần tóm tắt của mỗi bài viết
    @abstractmethod
    def _get_summary(self, html):
        pass

    # Trả về nội dung bài viết đã được chuẩn hóa
    @abstractmethod
    def _get_content(self, html):
        pass

    # Trả về nội dung bài viết được được xóa bỏ các thẻ html
    @abstractmethod
    def _get_plain(self, html):
        pass

    # Trả về url của ảnh đầu tiên trong bài viết
    @abstractmethod
    def _get_thumbnail(self, html):
        pass

    # Trả về tên tác giả bài viết
    @abstractmethod
    def _get_author(self, html):
        pass

    # Trả về danh sách các từ khóa của bài viết
    @abstractmethod
    def _get_tags(self, html):
        pass

    @abstractmethod
    def _parse(self, url, html, timeout=15):
        pass

    # Trả về tên miền của đầu báo mà nó xử lí
    def get_domain(self):
        return self._domain

    # Hàm phân tích trang và trả về các kết quả yêu cầu
    def parse(self, url, timeout=15):
        raw_html = get_html(url=url, timeout=timeout)
        if raw_html is None:
            raise Exception('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
        return self._parse(url=url, html=get_soup(raw_html), timeout=timeout)
