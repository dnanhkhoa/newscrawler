#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from abc import ABC, abstractmethod
from urllib.parse import urljoin

import requests
from requests import RequestException

from helpers import *


class BaseParser(ABC):
    def __init__(self):
        # Tên miền không có http://www dùng để nhận dạng url
        self._domain = None
        # Tên miền đầy đủ, không có / cuối cùng
        self._full_domain = None
        # Đăng ký các regex dùng để parse một số domain đặc biệt
        self._domain_regex = None
        # Biến chứa các hàm lambda hoặc con trỏ hàm giúp kế thùa linh động hơn.
        self._vars = {}
        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        self._vars['requests_cookies'] = {}

    # Tải nội dung web
    # OK
    def _get_html(self, url, timeout=15, attempts=3):
        if url is None:
            return None

        while attempts > 0:
            attempts -= 1
            try:
                response = requests.get(url=url, timeout=timeout, cookies=self._vars.get('requests_cookies'),
                                        allow_redirects=False)
                if response.status_code == requests.codes.ok:
                    return response.content.decode('UTF-8')
            except RequestException as e:
                logone.debug('URL: %s' % url)
                logone.exception(e)
        return None

    # Trả về URL tuyệt đối
    # OK
    # Tham số url làm segments hoặc url cần được đổi sang url tuyệt đối
    # Tham số domain đóng góp làm tiền tố  cho url tuyệt đối
    def _get_absolute_url(self, url, domain=None):
        if url is None:
            return None
        if domain is None:
            domain = self._full_domain
        return urljoin(domain, url)

    # Xử lí lưu các trang có chuyên mục con trong chuyên mục chính nhằm lặp đệ qui
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
    # Có thể dùng để chèn code lọc quảng cáo, bài viết liên quan
    @abstractmethod
    def _pre_process(self, html):
        pass

    # Hàm trả về (urls, stop) gồm danh sách các urls của bài đăng có trong trang từ from_date đến to_date
    # Tham số stop = True sẽ dừng việc duyệt trang (vượt quá ngày, không có bài viết nào)
    @abstractmethod
    def _get_urls_from_page(self, url, html, from_date=None, to_date=None, timeout=15):
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
    @abstractmethod
    def parse(self, url, from_date=None, to_date=None, timeout=15):
        pass
