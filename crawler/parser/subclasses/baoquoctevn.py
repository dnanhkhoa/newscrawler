#!/usr/bin/python
# -*- coding: utf8 -*-

from crawler.parser import *


class BaoQuocTeVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'baoquocte.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://baoquocte.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm thẻ cho biết trang nào đang active và dùng nó để dò địa chỉ trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_active_tag_func(html):
            div_tag = html.find('div', class_='grNextPage __MB_ARTICLE_PAGING')
            if div_tag is None:
                return None

            span_tags = div_tag.find_all('span', class_='current')
            return None if len(span_tags) == 0 else span_tags[-1]

        self._vars['get_active_tag_func'] = get_active_tag_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            # Thumbnail posts
            ul_tag = html.find('ul', class_='listitemNewsHot')
            if ul_tag is not None:
                a_tag = ul_tag.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append((a_tag.get('href'), None))

            # Other posts
            ul_tag = html.find('ul', class_='listingMainHot')
            if ul_tag is not None:
                posts = ul_tag.find_all('li', recursive=False)
                for post in posts:
                    a_tag = post.find('a', attrs={'href': True})
                    if a_tag is not None:
                        urls.append((a_tag.get('href'), None))

            # Child posts
            ul_tag = html.find('ul', id='listingGrNews')
            if ul_tag is None:
                return urls

            posts = ul_tag.find_all('li', recursive=False)
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                time_tag = post.find('div', class_='dateItem')
                if a_tag is not None and time_tag is not None:
                    time = time_tag.text.strip()
                    urls.append((a_tag.get('href'), datetime.strptime(time, '%H:%M | %d/%m/%Y')))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            div_tag = html.find('div', class_='dateUp')
            return None if div_tag is None else div_tag

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            return datetime.strptime(string.strip(), '%H:%M | %d/%m/%Y')

        self._vars['get_datetime_func'] = get_datetime_func

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

    # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
    # def _pre_process(self, html):
    #     return super()._pre_process(html)
