#!/usr/bin/python
# -*- coding: utf8 -*-

# Done

class BaseChecker(object):
    def __init__(self):
        # Tên miền không có http://www dùng để nhận dạng url
        self._domain = None
        # Đăng ký các regex dùng để parse một số domain đặc biệt
        self._domain_regex = None
        # Biến chứa các hàm lambda hoặc con trỏ hàm giúp kế thùa linh động hơn.
        self._vars = {}
        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        self._vars['requests_cookies'] = {}

    # Tải nội dung web
    def _get_html(self, url, timeout=15, attempts=3):
        assert url is not None, 'Tham số url không được là None'
        while attempts > 0:
            try:
                response = requests.get(url=url, timeout=timeout, cookies=self._vars.get('requests_cookies'),
                                        allow_redirects=False)
                return response.status_code == requests.codes.ok
            except RequestException as e:
                pass
            attempts -= 1
        return False

    # Trả về tên miền của đầu báo mà nó xử lí
    def get_domain(self):
        return self._domain

    # Trả về danh sách các regex dùng để parse url sao cho trỏ đúng vào class tương ứng
    def get_domain_regex(self):
        return self._domain_regex

    # Hàm kiểm tra url có live hay không
    def check(self, url, timeout=15, attempts=3):
        return self._get_html(url=url, timeout=timeout, attempts=attempts)
