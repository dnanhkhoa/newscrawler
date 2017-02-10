#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from datetime import date, datetime, timedelta

from crawler.parser import BaseParser
from helpers import *


class SubBaseParser(BaseParser):
    def __init__(self):
        super().__init__()

    # Hàm lấy ngày giờ của bài viết
    def _get_date_from_post(self, url, timeout=15):
        get_time_tag_func = self._vars.get('get_time_tag_func')
        get_datetime_func = self._vars.get('get_datetime_func')
        if get_time_tag_func is None or get_datetime_func is None:
            return None

        raw_html = get_html(url=url, timeout=timeout)
        if raw_html is None:
            log('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
            return None

        html = get_soup(raw_html)

        # Tìm được thẻ wrap chuỗi time -> lấy được time
        time_tag = get_time_tag_func(html)
        if time_tag is None:
            return None

        # Hàm datetime_func sẽ format time theo định dạng chỉ định
        return get_datetime_func(normalize_string(time_tag.text))

    # Hàm duyệt tìm các urls của bài viết trong trang
    def _get_urls_from_page(self, url, html, from_date=None, to_date=None, timeout=15):
        urls = []
        stop = False

        get_post_urls_func = self._vars.get('get_post_urls_func')
        if get_post_urls_func is None:
            stop = True
        else:
            post_urls = get_post_urls_func(html)
            if post_urls is None or len(post_urls) == 0:
                stop = True
            else:
                post_urls = [self._get_absolute_url(url=post_url, domain=url) for post_url in post_urls]

                last_post_date = self._get_date_from_post(url=post_urls[-1], timeout=timeout)
                if from_date > last_post_date:
                    stop = True
                    for post_url in post_urls:
                        current_post_date = self._get_date_from_post(url=post_url, timeout=timeout)
                        if from_date <= current_post_date <= to_date:
                            urls.append(post_url)
                else:  # from_date <= last_post_date:
                    first_post_date = self._get_date_from_post(url=post_urls[0], timeout=timeout)
                    if first_post_date <= to_date:
                        urls.extend(post_urls)
                    else:
                        for post_url in post_urls[1:]:
                            current_post_date = self._get_date_from_post(url=post_url, timeout=timeout)
                            if current_post_date <= to_date:
                                urls.append(post_url)
        return urls, stop

    # Hàm tiền xử lí trước khi gọi hàm get_urls_from_page
    # Kế thừa lại để xóa rác
    def _pre_process(self, html):
        return html

    # Hàm lấy nội dung trang hiện tại và url đến trang kế tiếp
    def _get_next_page(self, url, timeout=15):
        get_active_tag_func = self._vars.get('get_active_tag_func')
        if get_active_tag_func is None:
            return None

        raw_html = get_html(url=url, timeout=timeout)
        if raw_html is None:
            log('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
            return None

        html = get_soup(raw_html)

        active_tag = get_active_tag_func(html)
        if active_tag is None:
            return None

        # Lấy thẻ a anh em kế bên nhằm tìm link đến trang kế
        next_page = active_tag.find_next_sibling('a')
        # Có 1 số trường hợp dùng link tương đối cần chuyển sang tuyệt đối
        next_url = None if next_page is None else self._get_absolute_url(url=next_page.get('href'), domain=url)

        return html, next_url

    # Hàm trả về danh sách các urls chuyên mục con bên trong url của chuyên mục chính
    # Nếu không override get_child_category_section_func thì mặc định sẽ không duyệt chuyên mục con
    def _get_child_category_urls(self, url, timeout=15):
        get_child_category_section_func = self._vars.get('get_child_category_section_func')
        if get_child_category_section_func is not None:
            raw_html = get_html(url=url, timeout=timeout)
            if raw_html is None:
                log('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
                return None

            html = get_soup(raw_html)

            child_category_section = get_child_category_section_func(html)
            if child_category_section is not None:
                # Tự tìm tất cả thẻ a bên trong
                a_tags = child_category_section.find_all('a', attrs={'href': True})

                if len(a_tags) > 0:
                    urls = []
                    for a_tag in a_tags:
                        urls.append(self._get_absolute_url(url=a_tag.get('href'), domain=url))
                    return urls

        return [url]

    def parse(self, url, from_date=None, to_date=None, timeout=15):
        urls = []

        if from_date is None:
            from_date = datetime.combine(date.today(), datetime.min.time())
        if to_date is None:
            to_date = datetime.combine(date.today(), datetime.max.time())

        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, '%Y-%m-%d')

        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(microseconds=1)

        if from_date > to_date:
            log('Ngày nhập vào không hợp lệ (from_date > to_date)!')
            return urls

        # Lấy urls các chuyên mục con
        child_category_urls = self._get_child_category_urls(url=url, timeout=timeout)
        if child_category_urls is None:
            return urls

        child_category_urls = list(set(child_category_urls))

        # Lặp qua từng chuyên mục con
        for child_category_url in child_category_urls:

            next_url = child_category_url

            while True:
                # Lấy thông tin trang hiện tại và link đến trang kế tiếp
                page = self._get_next_page(url=next_url, timeout=timeout)
                if page is None:
                    break

                html, url = page
                html = self._pre_process(html=html)
                if html is None:
                    break

                urls_from_page, stop = self._get_urls_from_page(url=url, html=html, from_date=from_date,
                                                                to_date=to_date, timeout=timeout)

                urls.extend(urls_from_page)

                # Không còn trang kế tiếp nữa thì dừng
                if stop or url is None:
                    break

                next_url = url

        # Trả về danh sách các urls
        return urls
