#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
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
        self._vars['get_post_urls_func'] = lambda x: x

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
        source = []
        page_id = 0

        if isinstance(url, tuple):
            category_id, page_id = url
        else:
            raw_html = self._get_html(url=url, timeout=timeout)
            if raw_html is None:
                log('Không thể tải mã nguồn HTML từ địa chỉ %s' % url)
                return None

            category_id_regex = regex.compile(r"var catid = '([^']+)'", regex.IGNORECASE)
            matcher = category_id_regex.search(raw_html)
            if matcher is None:
                return None

            category_id = matcher.group(1)

            html = get_soup(raw_html)
            div_tag = html.find('div', class_='p-news-modtop')
            if div_tag is not None:
                a_tag = div_tag.find('a', attrs={'href': True})
                time_tag = div_tag.find('p', class_='fon3')
                if a_tag is not None and time_tag is not None:
                    time = time_tag.text.strip()
                    parts = time.split(' ')[:-1]
                    source.append((a_tag.get('href'), datetime.strptime(' '.join(parts), '%d/%m/%Y %H:%M')))

        data = self._get_posts(category_id=category_id, page_id=page_id)
        if data is None:
            return None

        data = json.loads(data, encoding='UTF-8')
        data = data.get('d')
        if data is not None or len(data.strip()) > 0:
            html = get_soup(data).body
            item_tags = html.find_all('div', class_='item')
            for item_tag in item_tags:
                a_tag = item_tag.find('a', attrs={'href': True})
                time_tag = item_tag.find('p', class_='fon3')
                if a_tag is not None and time_tag is not None:
                    time = time_tag.text.strip()
                    parts = time.split(' ')[:-1]
                    source.append((a_tag.get('href'), datetime.strptime(' '.join(parts), '%d/%m/%Y %H:%M')))

        return source, (category_id, page_id + 1)

    def _get_absolute_url(self, url, domain=None):
        return url

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
