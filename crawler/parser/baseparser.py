#!/usr/bin/python
# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup


class BaseParser(ABC):
    def __init__(self):
        self._domain = None

    def get_domain(self):
        return self._domain

    @abstractmethod
    def get_category_urls(self, html):
        pass

    @abstractmethod
    def get_urls(self, html, date):
        pass

    # Hàm phân tích trang và trả về danh sách các URLs có trong URL chủ đề
    def parse(self, url, date=None, timeout=15):
        raw_html = self.get_html(url=url, timeout=timeout, allow_redirects=False)
        if raw_html is None:
            raise Exception('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)

        html = BeautifulSoup(raw_html, 'html5lib')

        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        result = []

        category_urls = self.get_category_urls(html=html)
        if category_urls is None:
            urls = self.get_urls(html=html, date=date)
            if urls is not None:
                result.extend(urls)
        else:
            for category_url in category_urls:
                raw_html = self.get_html(url=category_url, timeout=timeout, allow_redirects=False)
                if raw_html is None:
                    raise Exception('Không thể tải mã nguồn HTML từ địa chỉ danh mục con %s' % url)
                else:
                    html = BeautifulSoup(raw_html, 'html5lib')
                    urls = self.get_urls(html=html, date=date)
                    if urls is not None:
                        result.extend(urls)
        return result
