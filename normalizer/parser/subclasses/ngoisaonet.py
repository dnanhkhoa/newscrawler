#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from normalizer.parser import *


class NgoiSaoNetParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Tên trang web sử dụng kiểu Title Case
        self._source_page = 'Ngôi Sao'

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'ngoisao.net'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://ngoisao.net'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        self._sub_url_regex = regex.compile(r'\d+-p\d+\.html', regex.IGNORECASE)
        self._video_regex = regex.compile(r"var videoSource = '([^']+)'", regex.IGNORECASE)
        self._video_thumbnail_regex = regex.compile(r"var thumbnail_url = '([^']+)'", regex.IGNORECASE)

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm thẻ chứa tiêu đề
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        self._vars['get_title_tag_func'] = lambda x: x.find('h1', class_='title')

        # Tìm thẻ chứa nội dung tóm tắt
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        self._vars['get_summary_tag_func'] = lambda x: x.find('p', class_='lead')

        # Tìm thẻ chứa danh sách các thẻ a chứa keyword bên trong
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        self._vars['get_tags_tag_func'] = lambda x: x.find('div', class_='block_tag')

        # Tìm thẻ chứa chuỗi thời gian đăng bài
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            return html.find('span', class_='spanDateTime')

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Định dạng chuỗi thời gian và trả về đối tượng datetime
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            string = string.split(',')[1]
            parts = string.strip().split(' ')[:-1]
            return datetime.strptime(' '.join(parts), '%d/%m/%Y %H:%M')

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
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', class_='fck_detail')

        # Chỉ định thẻ chứa tên tác giả
        # Khi sử dụng thẻ này thì sẽ tự động không sử dụng tính năng tự động nhận dạng tên tác giả
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_author_tag_func'] =

        # Chỉ định các nhãn được phép và không được phép dùng để dự đoán author
        # Các nhãn: author, center, right, bold, italic
        # Phân cách nhau bởi dấu | và những nhãn nào không được phép thì có tiền tố ^ ở đầu
        # Ví dụ: 'right|bold|author|^center|^italic'
        self._vars['author_classes_pattern'] = 'right|author'

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
        video_tags = html.find_all('div', attrs={'data-component-type': 'video', 'data-component-value': True})
        for video_tag in video_tags:
            video_id = video_tag.get('data-component-value')
            source = self._get_html('http://ngoisao.net/parser_v3.php?t=2&ft=video&id=%s' % video_id, timeout=timeout)
            if source is not None:
                video_thumbnail_url = default_thumbnail_url
                thumbnail_matcher = self._video_thumbnail_regex.search(source)
                if thumbnail_matcher is not None:
                    thumbnail_url = thumbnail_matcher.group(1)
                    if self._is_valid_image_url(url=thumbnail_url):
                        video_thumbnail_url = thumbnail_url

                matcher = self._video_regex.search(source)
                if matcher is not None:
                    video_url = matcher.group(1)
                    new_video_tag = create_video_tag(src=video_url, thumbnail=video_thumbnail_url,
                                                     mime_type=self._get_mime_type_from_url(url=video_url))
                    video_tag.insert_before(new_video_tag)

            video_tag.decompose()

        return super()._handle_video(html, default_thumbnail_url, timeout)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _pre_process(self, html):
        if html is None:
            return None

        page = html.find_parent('html')
        if page is not None:
            meta_url = page.find('meta', attrs={'property': 'og:url', 'content': True})
            if meta_url is not None:
                page_url = meta_url.get('content')
                main_matcher = self._sub_url_regex.search(page_url)
                if '/tin-tuc/trac-nghiem/' in page_url and main_matcher is None:
                    a_tags = html.find_all('a', attrs={'href': True})
                    url_map = {}
                    filtered_tags = []
                    for a_tag in a_tags:
                        sub_url = a_tag.get('href')
                        matcher = self._sub_url_regex.search(sub_url)
                        if '/tin-tuc/trac-nghiem/' in sub_url and matcher is not None:
                            if url_map.get(sub_url, False) is False:
                                url_map[sub_url] = True
                                filtered_tags.append((a_tag, sub_url))
                    for a_tag, sub_url in filtered_tags:
                        result = self.parse(url=sub_url)
                        if not result.is_ok():
                            continue
                        sub_content = result.get_content()['Content']
                        sub_content = get_soup(sub_content).body
                        sub_content.name = 'div'
                        a_tag.insert_before(sub_content)

        tags = html.find_all('div', class_='xemthem_new_ver width_common')
        for tag in tags:
            tag.decompose()

        return super()._pre_process(html)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _post_process(self, html):
        tags = html.find_all('div', recursive=False)
        for tag in tags:
            content = normalize_string(tag.text)
            if content.startswith('>>') or content.startswith('<<'):
                tag.decompose()
        return super()._post_process(html)

    @staticmethod
    def get_author_tag_func(html):
        div_tag = html.find('div', class_='author_mail')
        if div_tag is None:
            return None
        return div_tag.find('strong')

    def _get_author(self, html):
        authors = []
        author = super()._get_author(html)
        if author is not None:
            authors.append(author)

        self._vars['get_author_tag_func'] = self.get_author_tag_func
        author = super()._get_author(html)
        if author is not None:
            authors.append(author)
        self._vars['get_author_tag_func'] = None

        return '\n'.join(authors)
