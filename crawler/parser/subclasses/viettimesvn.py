#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class VietTimesVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'viettimes.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://viettimes.vn'

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
            a_tag = html.find('a', attrs={'id': 'ctl00_mainContent_ContentList1_pager_nextControl', 'href': True})
            return None if a_tag is None else a_tag.get('href')

        self._vars['get_next_url_func'] = get_next_url_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            div_tag = html.find('section', class_='cate-highlight')
            if div_tag is not None:
                # Other posts
                posts = div_tag.find_all('article', class_='story')
                for post in posts:
                    a_tag = post.find('a', attrs={'href': True})
                    if a_tag is not None:
                        urls.append(a_tag.get('href'))

            # Child posts
            div_tag = html.find('section', class_='cate-list-news')
            if div_tag is None:
                return urls

            div_tag = div_tag.find('div', class_='content')
            if div_tag is None:
                return urls

            posts = div_tag.find_all('article', class_='story')
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            div_tag = html.find('div', class_='author-time')
            if div_tag is None:
                return None
            return div_tag.find('time')

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            time_matcher = regex.search(r'(\d{2}:\d{2})', string, regex.IGNORECASE)
            date_matcher = regex.search(r'(\d{1,2}\/\d{1,2}\/\d{4})', string, regex.IGNORECASE)
            if time_matcher is None or date_matcher is None:
                return None
            return datetime.strptime('%s %s' % (date_matcher.group(1), time_matcher.group(1)), '%d/%m/%Y %H:%M')

        self._vars['get_datetime_func'] = get_datetime_func

    # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
    # def _pre_process(self, html):
    #     return super()._pre_process(html)

    def _get_html(self, url, timeout=15, attempts=3):
        assert url is not None, 'Tham số url không được là None'
        while attempts > 0:
            try:
                response = requests.get(url=url, timeout=timeout, cookies=self._vars.get('requests_cookies'),
                                        allow_redirects=True)
                if response.status_code == requests.codes.ok:
                    return response.content.decode('UTF-8')
            except RequestException as e:
                debug(url)
                log(e)
            attempts -= 1
        return None
