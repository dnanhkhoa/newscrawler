#!/usr/bin/python
# -*- coding: utf8 -*-

from crawler.parser import *


class NongNghiepVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'nongnghiep.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://nongnghiep.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

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
        def get_post_urls_func(html):
            urls = []

            # Thumbnail posts
            div_tag = html.find('div', class_='nn-row-main')
            if div_tag is not None:
                main_tag = div_tag.find('div', class_='nn-content')
                if main_tag is not None:
                    a_tag = main_tag.find('a', attrs={'href': True})
                    if a_tag is not None:
                        urls.append((a_tag.get('href'), None))

                sub_main_tag = div_tag.find('div', class_='nn-list-thumb-dt')
                if sub_main_tag is not None and sub_main_tag.ul is not None:
                    li_tags = sub_main_tag.ul.find_all('li', recursive=False)
                    for li_tag in li_tags:
                        a_tag = li_tag.find('a', attrs={'href': True})
                        if a_tag is not None:
                            urls.append((a_tag.get('href'), None))

            # Child posts
            div_tag = html.find('div', id='listScroll')
            if div_tag is None:
                return None

            ul_tag = div_tag.find('ul')
            if ul_tag is None:
                return None

            posts = ul_tag.find_all('li', recursive=False)
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                time_tag = post.find('span', class_='nn-time-post')
                if a_tag is not None and time_tag is not None:
                    time = time_tag.text.strip()
                    parts = time.split(' ')
                    urls.append((a_tag.get('href'), datetime.strptime(' '.join(parts[:-1]), '%d/%m/%Y, %H:%M')))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            return html.find('span', class_='nn-time-post')

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            parts = string.strip().split(' ')
            return datetime.strptime(' '.join(parts[:-1]), '%d/%m/%Y, %H:%M')

        self._vars['get_datetime_func'] = get_datetime_func

    # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
    # def _pre_process(self, html):
    #     return super()._pre_process(html)

    def _get_next_page(self, url, timeout=15):
        return super()._get_next_page(url, timeout)[0], url

    def _get_urls_from_page(self, url, html, from_date=None, to_date=None, timeout=15):
        url = '%s?date=%s&endate=%s' % (url, from_date.date().strftime('%d/%m/%Y'), to_date.date().strftime('%d/%m/%Y'))
        return super()._get_urls_from_page(url, html, from_date, to_date, timeout)[0], True
