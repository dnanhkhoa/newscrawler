#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from normalizer.parser import *


class BaoDatVietVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Tên trang web sử dụng kiểu Title Case
        self._source_page = 'Báo Đất Việt'

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'baodatviet.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://baodatviet.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm thẻ chứa tiêu đề
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_title_tag_func'] =

        # Tìm thẻ chứa nội dung tóm tắt
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_summary_tag_func'] =

        # Tìm thẻ chứa danh sách các thẻ a chứa keyword bên trong
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_tags_tag_func'] =

        # Tìm thẻ chứa chuỗi thời gian đăng bài
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            return html.find('p', class_='time')

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Định dạng chuỗi thời gian và trả về đối tượng datetime
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            string = string.split(',')[1]
            return datetime.strptime(string.strip(), '%d/%m/%Y %H:%M')

        self._vars['get_datetime_func'] = get_datetime_func

        # Chỉ định các nhãn có khả năng là caption
        # Gán bằng danh sách ['A', 'B', ..., 'Z']
        # Mặc định: ['desc', 'pic', 'img', 'box', 'cap', 'photo', 'hinh', 'anh']
        # self._vars['caption_classes'] =

        # Chỉ định các nhãn có khả năng là author
        # Gán bằng danh sách ['A', 'B', ..., 'Z']
        # Mặc định: ['author', 'copyright', 'source', 'nguon', 'tac-gia', 'tacgia']
        # self._vars['author_classes'] =

        # Chỉ định thẻ chứa nội dung chính
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', id='detail')

        # Chỉ định thẻ chứa tên tác giả
        # Khi sử dụng thẻ này thì sẽ tự động không sử dụng tính năng tự động nhận dạng tên tác giả
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_author_tag_func'] =

        # Chỉ định các nhãn được phép và không được phép dùng để dự đoán author
        # Các nhãn: author, center, right, bold, italic
        # Phân cách nhau bởi dấu | và những nhãn nào không được phép thì có tiền tố ^ ở đầu
        # Ví dụ: 'right|bold|author|^center|^italic'
        self._vars['author_classes_pattern'] = '^right|^center|^italic|bold|author'

        # Trả về url chứa hình ảnh thumbnail được lưu ở thẻ bên ngoài nội dung chính
        # Mặc định sẽ tự động nhận dạng
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_thumbnail_url_func'] =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

    # Hàm xử lí video có trong bài, tùy mỗi player mà có cách xử lí khác nhau
    # Khi xử lí xong cần thay thế thẻ đó thành thẻ video theo format qui định
    # Nếu cần tìm link trực tiếp của video trên youtube thì trong helper có hàm hỗ trợ
    def _handle_video(self, html, timeout=15):
        video_regex = regex.compile(r"ShowVideo\([^,]+,'([^']+)'", regex.IGNORECASE)
        script_tags = html.find_all('script')
        for script_tag in script_tags:
            matcher = video_regex.search(script_tag.text)
            if matcher is not None:
                video_url = matcher.group(1)
                video_tag = create_video_tag(src=video_url, mime_type=self._get_mime_type_from_url(url=video_url))
                script_tag.insert_before(video_tag)
            script_tag.decompose()
        return html

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _pre_process(self, html):
        tag = html.find('div', class_='bar-left_th')
        if tag is not None:
            tag.decompose()

        tag = html.find('h1', class_='title')
        if tag is not None:
            tag.decompose()

        tag = html.find('h2', class_='lead')
        if tag is not None:
            tag.decompose()

        tag = html.find('ul', class_='ul_relate')
        if tag is not None:
            tag.decompose()

        tag = html.find('div', id='AdAsia')
        if tag is not None:
            next_tag = tag.next_sibling
            while next_tag is not None:
                current_tag = next_tag
                next_tag = next_tag.next_sibling
                if not isinstance(current_tag, NavigableString):
                    current_tag.decompose()
            tag.decompose()
        return super()._pre_process(html)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    # def _post_process(self, html):
    #     return html

    def _get_tags(self, html):
        return super()._get_meta_keywords(html)

        # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
        # def _pre_process(self, html):
        #     return super()._pre_process(html)
