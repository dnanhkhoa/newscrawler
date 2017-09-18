#!/usr/bin/python
# -*- coding: utf8 -*-

# Unstable version: Done
from crawler.parser import *


class NhanDanComVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'nhandan.com.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://www.nhandan.com.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

        self._post_date_regex = regex.compile(r'cách đây (\d+) giờ', regex.IGNORECASE)

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm URL của trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # Lưu ý hàm gồm 2 tham số (html, url)
        # self._vars['get_next_url_func'] =

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_post_urls_func'] =

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_time_tag_func'] =

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_datetime_func'] =

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_datetime_func'] =

        # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
        # def _pre_process(self, html):
        #     return super()._pre_process(html)

    def _get_urls_from_page(self, url, html, from_date=None, to_date=None, timeout=15):
        urls = []

        div_tags = html.find_all('div', attrs={'class': 'col-sm-12 col-xs-12', 'style': 'padding:0px;'})
        if len(div_tags) == 3:
            post_tags = div_tags[0].find_all('div', class_='media')
            for post_tag in post_tags:
                a_tag = post_tag.find('a', attrs={'href': True})
                post_date_tag = post_tag.find('small', class_='text-muted')
                if a_tag is not None and post_date_tag is not None:
                    post_date_matcher = self._post_date_regex.search(normalize_string(post_date_tag.text))
                    if post_date_matcher is not None and int(post_date_matcher.group(1)) < datetime.now().hour:
                        urls.append(self._get_absolute_url(url=a_tag.get('href'), domain=url))

            post_tags = div_tags[1].find_all('div', class_='media')
            for post_tag in post_tags:
                a_tag = post_tag.find('a', attrs={'href': True})
                post_date_tag = post_tag.find('small', class_='text-muted')
                if a_tag is not None and post_date_tag is not None:
                    post_date_matcher = self._post_date_regex.search(normalize_string(post_date_tag.text))
                    if post_date_matcher is not None and int(post_date_matcher.group(1)) < datetime.now().hour:
                        urls.append(self._get_absolute_url(url=a_tag.get('href'), domain=url))

            post_tags = div_tags[2].find_all('div', class_='media',
                                             style='margin:10px;padding-bottom: 10px;border-bottom: 1px solid #ccc')
            for post_tag in post_tags:
                a_tag = post_tag.find('a', attrs={'href': True})
                post_date_tag = post_tag.find('small', class_='text-muted')
                if a_tag is not None and post_date_tag is not None:
                    post_date_matcher = self._post_date_regex.search(normalize_string(post_date_tag.text))
                    if post_date_matcher is not None and int(post_date_matcher.group(1)) < datetime.now().hour:
                        urls.append(self._get_absolute_url(url=a_tag.get('href'), domain=url))

        return list(set(urls)), None
