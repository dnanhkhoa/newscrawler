#!/usr/bin/python
# -*- coding: utf8 -*-
import logging

import requests
from bs4 import BeautifulSoup


class BaseParser(object):
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

    # Hàm định dạng ngày của trang web thành định dạng chung của hệ thống để so sánh
    def format_date(self, date):
        pass

    # Hàm rút trích ra danh sách các URLs có trong URL chủ đề
    def get_urls(self, soup, date=None):
        urls = []
        return urls

    # Hàm phân tích trang và trả về danh sách các URLs có trong URL chủ đề
    def parse(self, url, date=None, timeout=15):
        html = self.get_html(url=url, timeout=timeout)
        if html is None:
            return Exception('Không tải được nội dung địa chỉ %s' % url)
        # data = none sẽ lấy ngày hiện tại
        soup = BeautifulSoup(html, 'html5lib')
        return self.get_urls(soup=soup, date=date)
