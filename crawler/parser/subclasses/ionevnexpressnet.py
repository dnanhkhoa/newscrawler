#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class IOneVnExpressNetParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'ione.vnexpress.net'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://ione.vnexpress.net'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm thẻ cho biết trang nào đang active và dùng nó để dò địa chỉ trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_active_tag_func(html):
            div_tag = html.find('div', id='pagination')
            if div_tag is None:
                return None

            a_tag = div_tag.find('a', class_='active')
            return None if a_tag is None else a_tag

        self._vars['get_active_tag_func'] = get_active_tag_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            div_tag = html.find('div', id='box_news_top')
            if div_tag is not None:
                # Thumbnail posts
                post_tag = div_tag.find('div', class_='block_news_big')
                if post_tag is not None:
                    a_tag = post_tag.find('a', attrs={'href': True})
                    if a_tag is not None:
                        urls.append(a_tag.get('href'))

                # Other posts
                div_tag = div_tag.find('div', class_='box_sub_hot_news')
                if div_tag is not None and div_tag.ul is not None:
                    posts = div_tag.ul.find_all('li', recursive=False)
                    for post in posts:
                        a_tag = post.find('a', attrs={'href': True})
                        if a_tag is not None:
                            urls.append(a_tag.get('href'))

            # Child posts
            ul_tag = html.find('ul', id='news_home')
            if ul_tag is None:
                return urls

            posts = ul_tag.find_all('li', recursive=False)
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            # Bỏ những link video
            filtered_urls = []
            for url in urls:
                if '/video/' in url:
                    continue
                filtered_urls.append(url)

            return filtered_urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            div_tag = html.find('div', class_='block_timer')
            return None if div_tag is None else div_tag

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            time = string.strip().replace('00:', '12:')
            return datetime.strptime(time, '%I:%M %p | %d/%m/%Y')

        self._vars['get_datetime_func'] = get_datetime_func

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

        # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
        # def _pre_process(self, html):
        #     return super()._pre_process(html)
