#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class BaseParser(ABC):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.domain = None

    # Tải nội dung web
    def get_html(self, url, timeout=15):
        try:
            response = requests.get(url=url, timeout=timeout)
            if response.status_code == requests.codes.ok:
                return response.content.decode('UTF-8')
        except Exception as e:
            self._logger.exception(e)
        return None

    @abstractmethod
    def get_category_urls(self, html):
        pass

    @abstractmethod
    def get_urls(self, html, date):
        pass

    # Hàm phân tích trang và trả về danh sách các URLs có trong URL chủ đề
    def parse(self, url, date=None, timeout=15):
        raw_html = self.get_html(url=url, timeout=timeout)
        if raw_html is None:
            raise Exception('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)

        html = BeautifulSoup(raw_html, 'html5lib')

        if date is None:
            date = datetime().now().strftime('%Y-%m-%d')

        urls = []

        category_urls = self.get_categories(html=html)
        if category_urls is None:
            urls.append(self.get_urls(html=html, date=date))
        else:
            for category_url in category_urls:
                raw_html = self.get_html(url=category_url, timeout=timeout)
                if raw_html is None:
                    raise Exception('Không thể tải mã nguồn HTML từ địa chỉ danh mục con %s' % url)
                else:
                    html = BeautifulSoup(raw_html, 'html5lib')
                    urls.append(self.get_urls(html=html, date=date))
        return urls
