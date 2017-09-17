#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class NdhVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'ndh.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://ndh.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

        self._url_regex = regex.compile(r'Moredata\.aspx\?pageIndex=(\d+)', regex.IGNORECASE)

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

            li_tags = html.body.find_all('li', recursive=False)
            for li_tag in li_tags:
                a_tag = li_tag.find('a', attrs={'href': True, 'class': None})
                time_tag = li_tag.find('div', class_='sub-time')
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

        # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
        # def _pre_process(self, html):
        #     return super()._pre_process(html)

    def _get_next_page(self, url, timeout=15):
        html = super()._get_next_page(url, timeout)[0]

        url_matcher = self._url_regex.search(url)
        if url_matcher is None:
            hidCatIdPage_tag = html.find('input', id='hidCatIdPage')
            hidIsEdition_tag = html.find('input', id='hidIsEdition')
            hidEditionID_tag = html.find('input', id='hidEditionID')
            if hidCatIdPage_tag is None or hidIsEdition_tag is None or hidEditionID_tag is None:
                return None

            url = 'http://ndh.vn/Handler/Moredata.aspx?pageIndex=%%d&Cat_ID=%s&isEdition=%s&Et=%s' % (
                hidCatIdPage_tag.get('value'), hidIsEdition_tag.get('value'), hidEditionID_tag.get('value'))
            return super()._get_next_page(url % 1, timeout)[0], url % 2

        next_url = url.replace(url_matcher.group(0), 'Moredata.aspx?pageIndex=%d' % (int(url_matcher.group(1)) + 1))
        return html, next_url
