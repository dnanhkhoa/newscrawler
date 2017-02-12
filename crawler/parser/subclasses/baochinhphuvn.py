#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class BaoChinhPhuVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'baochinhphu.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://baochinhphu.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm thẻ cho biết trang nào đang active và dùng nó để dò địa chỉ trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_active_tag_func(html):
            span_tag = html.find('span', id='ctl00_leftContent_ctl01_pager')
            if span_tag is None:
                return None

            a_tag = span_tag.find('a', class_='current')
            return None if a_tag is None else a_tag

        self._vars['get_active_tag_func'] = get_active_tag_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            # Thumbnail post (chỉ lấy ở trang 1)
            span_tag = html.find('span', id='ctl00_leftContent_ctl01_pager')
            if span_tag is not None:
                a_tag = span_tag.find('a', class_='current')
                if a_tag is not None and normalize_string(a_tag.text) == '1':
                    div_tag = html.find('div', class_='featured')
                    if div_tag is not None:
                        a_tag = div_tag.find('a', attrs={'href': True})
                        time_tag = div_tag.find('span', class_='time')
                        if a_tag is not None and time_tag is not None:
                            time = time_tag.text.strip()
                            urls.append((a_tag.get('href'), datetime.strptime(time, '%H:%M, %d/%m/%Y')))

            # Child posts
            div_tag = html.find('div', class_='zonelisting')
            if div_tag is None:
                return urls

            posts = div_tag.find_all('div', class_='story', recursive=False)
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                time_tag = post.find('span', class_='time')
                if a_tag is not None and time_tag is not None:
                    time = time_tag.text.strip()
                    urls.append((a_tag.get('href'), datetime.strptime(time, '%H:%M, %d/%m/%Y')))
            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_time_tag_func'] =
        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_datetime_func'] =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        self._vars['html_cookies'] = {}

        self._cookie_regex = regex.compile(r'<body><script>document\.cookie="([^=]+)=([^"]+)"', regex.IGNORECASE)

    # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
    # def _pre_process(self, html):
    #     return super()._pre_process(html)

    def _get_html(self, url, timeout=15, attempts=3):
        assert url is not None, 'Tham số url không được là None'
        while attempts > 0:
            try:
                response = requests.get(url=url, timeout=timeout, cookies=self._vars['html_cookies'],
                                        allow_redirects=False)
                if response.status_code == requests.codes.ok:
                    data = response.content.decode('UTF-8')
                    matcher = self._cookie_regex.search(data)
                    if matcher is not None:
                        cookie_name = matcher.group(1)
                        cookie_value = matcher.group(2)
                        self._vars['html_cookies'][cookie_name] = cookie_value
                        continue
                    return data
            except RequestException as e:
                log(e)
            attempts -= 1
        return None
