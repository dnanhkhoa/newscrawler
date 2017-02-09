#!/usr/bin/python
# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from urllib.parse import urljoin


class BaseParser(ABC):
    def __init__(self):
        self._domain = None
        self._domain_regex = None
        self._vars = {}

    # Trả về URL tuyệt đối
    def _get_absolute_url(self, url):
        return urljoin(self._domain, url)

    # Xử lí các trang có chuyên mục con trong chuyên mục chính
    @abstractmethod
    def _get_child_category_urls(self, url, timeout=15):
        pass

    # Hàm trả về (html, next_url) từ url hiện tại
    # Nếu không có trang kế thì next_url = None
    # Nếu không có nội dung hoặc lỗi thì trả về mỗi None
    @abstractmethod
    def _get_next_page(self, url, timeout=15):
        pass

    # Hàm được gọi trước khi gọi hàm get_urls_from_page
    # Có thể dùng để chèn code lọc quảng cáo
    @abstractmethod
    def _pre_process(self, html):
        pass

    @abstractmethod
    def get_urls_from_page(self, html, from_date=None, to_date=None):
        pass

    # Hàm trả về thời gian của bài đăng
    @abstractmethod
    def _get_date_from_post(self, url, timeout=15):
        pass

    # Trả về tên miền của đầu báo mà nó xử lí
    def get_domain(self):
        return self._domain

    # Trả về danh sách các regex dùng để parse url sao cho trỏ đúng vào class tương ứng
    def get_domain_regex(self):
        return self._domain_regex

    # Hàm phân tích trang và trả về danh sách các URLs có trong URL chủ đề
    def parse(self, url, from_date=None, to_date=None, timeout=15):
        pass
