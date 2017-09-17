#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class BizLiveVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'bizlive.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://bizlive.vn'

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
        def get_next_url_func(html, url):
            span_tag = html.find('span', id='ctl00_main_ContentListBizLive1_pager')
            if span_tag is None:
                return None
            a_tag = span_tag.find('a', attrs={'class': 'next', 'disabled': None, 'href': True})
            return None if a_tag is None else a_tag.get('href')

        self._vars['get_next_url_func'] = get_next_url_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            # Thumbnail posts
            div_tag = html.find('div', class_='mainContentLeft')
            if div_tag is not None:
                main_tag = div_tag.find('div', class_='col-440')
                if main_tag is not None:
                    a_tag = main_tag.find('a', attrs={'href': True})
                    if a_tag is not None:
                        urls.append(a_tag.get('href'))

                    li_tags = main_tag.find_all('li')
                    for li_tag in li_tags:
                        a_tag = li_tag.find('a', attrs={'href': True})
                        if a_tag is not None:
                            urls.append(a_tag.get('href'))

            div_tags = html.find_all('div', class_=lambda x: x and 'list-item-news-' in x)
            for div_tag in div_tags:
                if 'list-item-news-1' in div_tag.get('class'):
                    ul_tag = div_tag.find('ul')
                    if ul_tag is not None:
                        li_tags = ul_tag.find_all('li', recursive=False)
                        for li_tag in li_tags:
                            a_tag = li_tag.find('a', attrs={'href': True})
                            if a_tag is not None:
                                urls.append(a_tag.get('href'))
                else:
                    left_div_tag = div_tag.find('div', class_='FloatLeft')
                    if left_div_tag is not None:
                        li_tags = left_div_tag.find_all('li')
                        for li_tag in li_tags:
                            a_tag = li_tag.find('a', attrs={'href': True})
                            if a_tag is not None:
                                urls.append(a_tag.get('href'))

                    right_div_tag = div_tag.find('div', class_='FloatRight')
                    if right_div_tag is not None:
                        a_tag = right_div_tag.find('a', attrs={'href': True})
                        if a_tag is not None:
                            urls.append(a_tag.get('href'))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            author_tag = html.find('div', class_='author')
            return None if author_tag is None else author_tag.find('p', class_=None)

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            return datetime.strptime(string, '%H:%M %d/%m/%Y')

        self._vars['get_datetime_func'] = get_datetime_func

        # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
        # def _pre_process(self, html):
        #     return super()._pre_process(html)
