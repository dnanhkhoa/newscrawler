#!/usr/bin/python
# -*- coding: utf8 -*-

from copy import deepcopy

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
        self._full_domain = 'https://ngoisao.net'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        self._domain_regex = [regex.compile(r'video.(ngoisao.net)', regex.IGNORECASE)]

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
        # Tạo bộ parser riêng cho video
        video_parser = deepcopy(self)

        # Time
        def get_datetime_vid_func(string):
            string = string.split(',')[-1]
            parts = string.strip().split(' ')[:-1]
            return datetime.strptime(' '.join(parts), '%d/%m/%y %H:%M')

        video_parser._vars['get_datetime_func'] = get_datetime_vid_func

        def get_main_content_tag_vid_func(html):
            div_tag = html.find('div', class_='fck_detail')
            return div_tag and div_tag.div

        video_parser._vars['get_main_content_tag_func'] = get_main_content_tag_vid_func

        def get_author_tag_div_func(html):
            div_tag = html.find('p', class_='author_top')
            return div_tag and div_tag.strong

        video_parser._vars['get_author_tag_func'] = get_author_tag_div_func

        video_parser._vars['get_tags_tag_func'] = lambda x: x.find('div', id='box_tag')

        video_parser._pre_process = super(NgoiSaoNetParser, video_parser)._pre_process
        video_parser._post_process = super(NgoiSaoNetParser, video_parser)._post_process
        video_parser._get_author = super(NgoiSaoNetParser, video_parser)._get_author

        video_parser.parse_video = super(NgoiSaoNetParser, video_parser)._parse
        self._vars['video_parser'] = video_parser

    # Hàm xử lí video có trong bài, tùy mỗi player mà có cách xử lí khác nhau
    # Khi xử lí xong cần thay thế thẻ đó thành thẻ video theo format qui định
    # Nếu cần tìm link trực tiếp của video trên youtube thì trong helper có hàm hỗ trợ
    def _handle_video(self, html, default_thumbnail_url=None, timeout=15):
        video_tags = html.find_all('div', attrs={'data-component-type': 'video', 'data-component-value': True})
        for video_tag in video_tags:
            video_id = video_tag.get('data-component-value')
            source = self._get_html('https://ngoisao.net/parser_v3.php?t=2&ft=video&id=%s' % video_id, timeout=timeout)
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

        script_tags = html.find_all('script')
        if len(script_tags) > 0:
            first_script = script_tags[0]
            script_code = first_script.text

            # Thumbnail
            thumbnail_matcher = regex.search(r'thumbnail_url="([^"]+)"', script_code, regex.IGNORECASE)
            if thumbnail_matcher is not None:
                thumbnail_url = thumbnail_matcher.group(1)
                if self._is_valid_image_url(url=thumbnail_url):
                    video_thumbnail_url = thumbnail_url

            # Video URL
            matcher = regex.findall(r"videoSource\d+p = '([^']+)'", script_code, regex.IGNORECASE)
            if len(matcher) > 0:
                video_url = matcher[-1]
                new_video_tag = create_video_tag(src=video_url, thumbnail=video_thumbnail_url,
                                                 mime_type=self._get_mime_type_from_url(url=video_url))
                first_script.insert_before(new_video_tag)

            first_script.decompose()

        return super()._handle_video(html, default_thumbnail_url, timeout)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _pre_process(self, html):
        if html is None:
            return None

        url_queue = self._vars['url_queue']
        visited_urls = self._vars['visited_urls']

        table_stack = self._vars['table_stack'] = []

        page = html.find_parent('html')
        if page is not None:
            meta_url = page.find('meta', attrs={'property': 'og:url', 'content': True})
            if meta_url is not None:
                parent_url = meta_url.get('content')
                if '/tin-tuc/trac-nghiem/' in parent_url:
                    a_tags = html.find_all('a', attrs={'href': True})
                    for a_tag in a_tags:
                        child_url = a_tag.get('href')
                        child_url_matcher = self._sub_url_regex.search(child_url)
                        if '/tin-tuc/trac-nghiem/' in child_url and child_url_matcher is not None:
                            if child_url not in visited_urls:
                                # Thêm vào hàng đợi
                                url_queue.put((parent_url, child_url))

                            data_link = '/tin-tuc/s/%s' % self._get_alias(url=child_url)

                            # Sửa lại link
                            img_tags = a_tag.find_all('img')
                            for img_tag in img_tags:
                                img_tag['data-link'] = data_link

                            if len(normalize_string(a_tag.text)) > 0:
                                a_tag.name = 'video'
                                a_tag['data-link'] = data_link
                                a_tag['data-dummy'] = 'hyperlink'

                    table_tags = html.find_all('table', recursive=False)
                    for table_tag in table_tags:
                        video_tag = create_html_tag('video')
                        video_tag['data-dummy'] = 'table'
                        table_tag.wrap(video_tag)
                        table_stack.append(table_tag.extract())

        # Xóa bài viết liên quan
        # table_tags = html.find_all('table', class_='tbl_insert', recursive=False)
        # if len(table_tags) > 0:
        #     img_tag = table_tags[-1].find('img', attrs={'src': True})
        #     if img_tag is not None:
        #         img_src = img_tag.get('src')
        #         if self._get_image_size(url=img_src) == (200, 120):
        #             table_tags[-1].decompose()

        tags = html.find_all('div', class_='xemthem_new_ver width_common')
        for tag in tags:
            tag.decompose()

        return super()._pre_process(html)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _post_process(self, html):
        tags = html.find_all('div', recursive=False)
        for tag in tags:
            content = normalize_string(tag.text)
            if content.startswith('>>') or content.startswith('<<') or content.startswith(
                    'Xem thêm:') or content.startswith('Xem tiếp'):
                tag.decompose()

        table_stack = self._vars['table_stack']
        table_tags = html.find_all('video', attrs={'data-dummy': 'table'}, recursive=False)
        for table_tag in table_tags:
            if len(table_stack) > 0:
                table_tag.replace_with(table_stack.pop(0))

        link_tags = html.find_all('video', attrs={'data-dummy': 'hyperlink'})
        for link_tag in link_tags:
            attrs_before = link_tag.attrs
            link_tag.name = 'a'
            link_tag.attrs = {'href': attrs_before['data-link']}
            link_tag.wrap(create_html_tag('p'))

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

    def _parse(self, url, html, timeout=15):
        video_domain = 'video.ngoisao.net'
        if video_domain in url:
            div_tag = html.find('div', class_='video_hot')
            a_tag = div_tag and div_tag.find('a', attrs={'href': True})
            if a_tag is None:
                return None

            domain = self._full_domain.replace(self._domain, video_domain)
            video_page_url = self._get_absolute_url(url=a_tag.get('href'), domain=domain)
            raw_html = self._get_html(url=video_page_url, timeout=timeout)
            if raw_html is None:
                return None
            return self._vars['video_parser'].parse_video(url=video_page_url, html=get_soup(raw_html), timeout=timeout)

        return super()._parse(url, html, timeout)
