#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class InfoGameVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'infogame.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://infogame.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

        self._datetime_regex = regex.compile(r'(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2})', regex.IGNORECASE)

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm URL của trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # Lưu ý hàm gồm 2 tham số (html, url)
        def get_next_url_func(html, url):
            a_tags = html.find_all('a', attrs={'class': 'nextBtn', 'href': True})
            return a_tags[-1].get('href') if len(a_tags) > 0 else None

        self._vars['get_next_url_func'] = get_next_url_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            # Child posts
            div_tag = html.find('div', class_='danhsachtin')
            if div_tag is None:
                return None

            posts = div_tag.find_all('div', class_='tin1', recursive=False)
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                div_tag = post.find('div', class_='thongtin')
                if div_tag is None:
                    continue

                p_tags = div_tag.find_all('p', recursive=False)
                if a_tag is not None and len(p_tags) > 0:
                    time_string = p_tags[-1].text
                    matcher = self._datetime_regex.search(time_string)
                    if matcher is None:
                        continue

                    urls.append((a_tag.get('href'), datetime.strptime(matcher.group(1), '%d/%m/%Y %H:%M')))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_time_tag_func'] =

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_datetime_func'] =

        # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
        # def _pre_process(self, html):
        #     return super()._pre_process(html)
