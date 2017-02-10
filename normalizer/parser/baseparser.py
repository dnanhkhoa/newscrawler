#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from abc import ABC, abstractmethod
from datetime import datetime
from urllib.parse import urljoin

from helpers import *


class BaseParser(ABC):
    def __init__(self):
        # Tên trang web sử dụng kiểu Title Case
        self._source_page = None
        # Tên miền không có http://www dùng để nhận dạng url
        self._domain = None
        # Tên miền đầy đủ, không có / cuối cùng
        self._full_domain = None
        # Đăng ký các regex dùng để parse một số domain đặc biệt
        self._domain_regex = None
        # Biến chứa các hàm lambda hoặc con trỏ hàm giúp kế thùa linh động hơn.
        self._vars = {}

    # Trả về URL tuyệt đối
    def _get_absolute_url(self, url, domain=None):
        if domain is None:
            domain = self._full_domain
        return urljoin(domain, url)

    # Trả về alias từ url của bài viết
    def _get_alias(self, url):
        obj = urlparse(url)
        alias = obj.path.strip('/').split('/')[-1]
        return alias

    # Trả về image url hợp lệ
    def _get_valid_image_url(self, url, domain=None):
        image_url = self._get_absolute_url(url=url, domain=domain)
        cleaned_image_url = clean_url_query(url=image_url)
        if is_valid_image_url(cleaned_image_url):
            image_url = cleaned_image_url
        return image_url

    # Trả về kết quả có cấu trúc theo yêu cầu
    def _build_json(self, url=None, mobile_url=None, title=None, alias=None, meta_keywords=None, meta_description=None,
                    publish_date=None, author=None, tags=None, thumbnail=None, summary=None, content=None, plain=None):

        if mobile_url is None:
            mobile_url = url

        return {
            'sourcePage': '' if self._source_page is None else self._source_page,
            'title': '' if title is None else title,
            'alias': '' if alias is None else alias,
            'sourceUrl': '' if url is None else url,
            'sourceUrlMobile': '' if mobile_url is None else mobile_url,
            'author': '' if author is None else author,
            'thumbnail': '' if thumbnail is None else thumbnail,
            'tags': '' if tags is None else tags,
            'description': '' if summary is None else summary,
            'publishDate': '' if publish_date is None else format_datetime(publish_date),
            'metaDescription': '' if meta_description is None else meta_description,
            'metaKeywords': '' if meta_keywords is None else meta_keywords,
            'crawledDate': format_datetime(datetime.now()),
            'content': '' if content is None else content,
            'plainContent': '' if plain is None else plain
        }

    # Trả về mobile url của bài viết
    @abstractmethod
    def _get_mobile_url(self, html, url):
        pass

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

    # Trả về danh sách các regex dùng để parse url sao cho trỏ đúng vào class tương ứng
    def get_domain_regex(self):
        return self._domain_regex

    # Hàm phân tích trang và trả về các kết quả yêu cầu
    def parse(self, url, timeout=15):
        raw_html = get_html(url=url, timeout=timeout)
        if raw_html is None:
            log('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
            return None

        return self._parse(url=url, html=get_soup(raw_html, clear_special_chars=True), timeout=timeout)
