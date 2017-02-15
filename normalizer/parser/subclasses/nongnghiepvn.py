#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from normalizer.parser import *


class NongNghiepVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Tên trang web sử dụng kiểu Title Case
        self._source_page = 'Nông Nghiệp'

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'nongnghiep.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://nongnghiep.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        self._video_regex = regex.compile(r'urlfile=([^&]+)&', regex.IGNORECASE)
        self._main_video_regex = regex.compile(r"file: '([^']+)'", regex.IGNORECASE)
        self._video_thumbnail_regex = regex.compile(r"image: '([^']+)'", regex.IGNORECASE)

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
            return html.find('span', attrs={'itemprop': 'datePublished'})

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Định dạng chuỗi thời gian và trả về đối tượng datetime
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            time = string.strip()
            parts = time.split(' ')[:-1]
            return datetime.strptime(' '.join(parts), '%d/%m/%Y, %H:%M')

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
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', attrs={'itemprop': 'articleBody'})

        # Chỉ định thẻ chứa tên tác giả
        # Khi sử dụng thẻ này thì sẽ tự động không sử dụng tính năng tự động nhận dạng tên tác giả
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_author_tag_func(html):
            div_tag = html.find('div', class_='content')
            if div_tag is None:
                return None
            return div_tag.find('span', style='text-transform: uppercase; font-weight: bold;')

        self._vars['get_author_tag_func'] = get_author_tag_func

        # Chỉ định các nhãn được phép và không được phép dùng để dự đoán author
        # Các nhãn: author, center, right, bold, italic
        # Phân cách nhau bởi dấu | và những nhãn nào không được phép thì có tiền tố ^ ở đầu
        # Ví dụ: 'right|bold|author|^center|^italic'
        # self._vars['author_classes_pattern'] =

        # Chỉ định tự động xóa tất cả các chuỗi bên dưới tác giả
        # Thích hợp khi bài viết chèn nhiều quảng cảo, links bên dưới mà không có id để xóa
        # Gán bằng True / False
        # self._vars['clear_all_below_author'] = True

        # Trả về url chứa hình ảnh thumbnail được lưu ở thẻ bên ngoài nội dung chính
        # Mặc định sẽ tự động nhận dạng
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_thumbnail_url_func'] =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

    # Hàm xử lí video có trong bài, tùy mỗi player mà có cách xử lí khác nhau
    # Khi xử lí xong cần thay thế thẻ đó thành thẻ video theo format qui định
    # Nếu cần tìm link trực tiếp của video trên youtube thì trong helper có hàm hỗ trợ
    def _handle_video(self, html, default_thumbnail_url=None, timeout=15):
        div_tag = html.find_parent('div', class_='p-news-detail')
        if div_tag is not None:
            div_tag = div_tag.find('div', class_='fixmod')
            if div_tag is not None:
                div_tag = div_tag.find('div', class_='image')
                if div_tag is not None:
                    video_thumbnail_url = default_thumbnail_url

                    script_content = div_tag.text

                    thumbnail_matcher = self._video_thumbnail_regex.search(script_content)
                    if thumbnail_matcher is not None:
                        thumbnail_url = thumbnail_matcher.group(1)
                        if self._is_valid_image_url(url=thumbnail_url):
                            video_thumbnail_url = thumbnail_url

                    video_matcher = self._main_video_regex.search(script_content)
                    if video_matcher is not None:
                        video_url = video_matcher.group(1)
                        new_video_tag = create_video_tag(src=video_url, thumbnail=video_thumbnail_url,
                                                         mime_type=self._get_mime_type_from_url(url=video_url))
                        html.insert(0, new_video_tag)

        video_tags = html.find_all('iframe', attrs={'class': 'iframebnncontentsmp4', 'src': True})
        for video_tag in video_tags:
            video_matcher = self._video_regex.search(video_tag.get('src'))
            if video_matcher is None:
                video_tag.decompose()
            else:
                video_url = 'http://image.nongnghiep.vn/upload%s' % video_matcher.group(1)
                new_video_tag = create_video_tag(src=video_url, thumbnail=default_thumbnail_url,
                                                 mime_type=self._get_mime_type_from_url(url=video_url))

                video_tag.replace_with(new_video_tag)

        return super()._handle_video(html, default_thumbnail_url, timeout)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    # def _pre_process(self, html):
    #     return super()._pre_process(html)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    # def _post_process(self, html):
    #     return html

    def _get_mobile_url(self, url):
        return url.replace('nongnghiep.vn', 'm.nongnghiep.vn')

    def _get_tags(self, html):
        return super()._get_meta_keywords(html)

    def _get_og_image(self, html):
        return super()._get_og_image(html).replace('nongnghiep.vn', 'image.nongnghiep.vn')
