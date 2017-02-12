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

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm thẻ cho biết trang nào đang active và dùng nó để dò địa chỉ trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_active_tag_func'] =

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

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

    # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
    # def _pre_process(self, html):
    #     return super()._pre_process(html)

    def _get_next_page(self, url, timeout=15):
        raw_html = self._get_html(url=url, timeout=timeout)
        if raw_html is None:
            log('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
            return None



        #data = self._get_posts(category_id=9, page_id=0)

        return None

    def _get_urls_from_page(self, url, html, from_date=None, to_date=None, timeout=15):
        pass

    def _get_posts(self, category_id, page_id, timeout=15):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = {
            'catid': category_id,
            'date': '',
            'enddate': '',
            'pageindex': page_id
        }
        response = requests.post(url='http://nongnghiep.vn///Ajaxloads/ServiceData.asmx/GetNewsDataScrollNews',
                                 headers=headers, data=json.dumps(data), timeout=timeout, allow_redirects=True)
        if response.status_code == requests.codes.ok:
            return response.content.decode('UTF-8')
        return None
