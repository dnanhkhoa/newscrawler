#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from checker.basecheckers import *


class HaNoiMoiComVnChecker(BaseChecker):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'hanoimoi.com.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

    # Tải nội dung web
    def _is_live(self, url, timeout=15, attempts=3):
        assert url is not None, 'Tham số url không được là None'
        while attempts > 0:
            try:
                attempts -= 1

                response = requests.get(url=url, timeout=timeout, cookies=self._vars.get('requests_cookies'))
                status_code = response.status_code
                history = response.history

                if len(history) > 0:
                    location = history[-1].headers.get('location')
                    matcher = self._bad_link_regex.search(location)
                    return matcher is None

                return status_code < 300 or status_code >= 500
            except RequestException as e:
                pass
        return True
