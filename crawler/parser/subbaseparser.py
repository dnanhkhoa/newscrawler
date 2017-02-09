#!/usr/bin/python
# -*- coding: utf8 -*-
from crawler.parser import BaseParser
from helpers import *


class SubBaseParser(BaseParser):
    def __init__(self):
        super().__init__()

    def _get_date_from_post(self, url, timeout=15):
        pass

    def get_urls_from_page(self, html, from_date=None, to_date=None, timeout=15):
        pass

    def _pre_process(self, html):
        pass

    def _get_next_page(self, url, timeout=15):
        raw_html = get_html(url=url, timeout=timeout)
        if raw_html is None:
            raise Exception('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
        html = get_soup(raw_html)


    def _get_child_category_urls(self, url, timeout=15):
        get_child_category_section_func = self._vars.get('get_child_category_section_func')
        if get_child_category_section_func is not None:
            raw_html = get_html(url=url, timeout=timeout)
            if raw_html is None:
                raise Exception('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)

            html = get_soup(raw_html)
            child_category_section = get_child_category_section_func(html)
            if child_category_section is not None:
                urls = []
                for a_tag in child_category_section.find_all('a', attrs={'href': True}):
                    urls.append(a_tag.get('href'))
                return urls

        return [url]

    def parse(self, url, from_date=None, to_date=None, timeout=15):
        urls = []

        child_category_urls = self._get_child_category_urls(url=url, timeout=timeout)
        if child_category_urls is None:
            return urls

        for child_category_url in child_category_urls:
            while True:
                page = self._get_next_page(url=child_category_url, timeout=timeout)
                if page is None:
                    break


        # Trả về danh sách các urls
        return urls
