#!/usr/bin/python
# -*- coding: utf8 -*-

from crawler.parser import *


class HaNoiMoiComVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'hanoimoi.com.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://hanoimoi.com.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm thẻ cho biết trang nào đang active và dùng nó để dò địa chỉ trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_active_tag_func(html):
            div_tag = html.find('div', class_='paging')
            if div_tag is None:
                return None

            li_tag = div_tag.find('li', class_='next')
            if li_tag is not None:
                li_tag.decompose()

            li_tags = div_tag.find_all('li')
            for li_tag in li_tags:
                li_tag.unwrap()

            b_tag = div_tag.find('b')
            return None if b_tag is None else b_tag

        self._vars['get_active_tag_func'] = get_active_tag_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            # Thumbnail posts
            div_tags = html.find_all('div', class_='timeline')
            for div_tag in div_tags:
                a_tag = div_tag.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            # Child posts
            posts = html.find_all('li', class_='bdrtp')
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))
            print(urls)
            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            div_tag = html.find('div', class_='moder')
            if div_tag is None:
                return None
            div_tag = div_tag.find('div', class_='refer')
            if div_tag is None:
                return None
            a_tag = div_tag.find('a', class_='cap')
            if a_tag is not None:
                a_tag.decompose()
            return div_tag

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            time_matcher = regex.search(r'(\d{2}:\d{2})', string, regex.IGNORECASE)
            date_matcher = regex.search(r'(\d{2}\/\d{2}\/\d{4})', string, regex.IGNORECASE)
            if time_matcher is None or date_matcher is None:
                return None
            print(datetime.strptime('%s %s' % (date_matcher.group(1), time_matcher.group(1)), '%d/%m/%Y %H:%M'))
            return datetime.strptime('%s %s' % (date_matcher.group(1), time_matcher.group(1)), '%d/%m/%Y %H:%M')

        self._vars['get_datetime_func'] = get_datetime_func

        # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
        # def _pre_process(self, html):
        #     return super()._pre_process(html)
