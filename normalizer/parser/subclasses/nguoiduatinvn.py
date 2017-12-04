#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from normalizer.parser import *


class NguoiDuaTinVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Tên trang web sử dụng kiểu Title Case
        self._source_page = 'Người Đưa Tin'

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'nguoiduatin.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://www.nguoiduatin.vn'

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
        self._vars['get_tags_tag_func'] = lambda x: x.find('div', class_='display-tags')

        # Tìm thẻ chứa chuỗi thời gian đăng bài
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            author_tag = html.find('div', class_='datetime upcase')
            return None if author_tag is None else author_tag.find('p', class_='upcase')

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Định dạng chuỗi thời gian và trả về đối tượng datetime
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            return datetime.strptime(string, '%H:%M %d/%m/%Y')

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
        self._vars['get_main_content_tag_func'] = lambda x: x.find('div', class_='article-content')

        # Chỉ định thẻ chứa tên tác giả
        # Khi sử dụng thẻ này thì sẽ tự động không sử dụng tính năng tự động nhận dạng tên tác giả
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_author_tag_func'] =

        # Chỉ định các nhãn được phép và không được phép dùng để dự đoán author
        # Các nhãn: author, center, right, bold, italic
        # Phân cách nhau bởi dấu | và những nhãn nào không được phép thì có tiền tố ^ ở đầu
        # Ví dụ: 'right|bold|author|^center|^italic'
        self._vars['author_classes_pattern'] = 'bold'

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
        video_tags = html.find_all('div', class_='content_mecloud')
        for video_tag in video_tags:
            script_tag = video_tag.find('script', attrs={'src': True})
            if script_tag is not None:
                source = self._get_html(url=script_tag.get('src'), timeout=timeout)
                if source is not None:
                    matcher = regex.findall(r'src="([^"]+)"', source)
                    if len(matcher) > 0:
                        source = self._get_html(url=matcher[-1], timeout=timeout)
                        if source is not None:
                            # Thumbnail
                            thumbnail_matcher = regex.search(r'"thumbnail":"([^"]+)"', source, regex.IGNORECASE)
                            if thumbnail_matcher is not None:
                                thumbnail_url = thumbnail_matcher.group(1)
                                if 'https:' not in thumbnail_url:
                                    thumbnail_url = 'https:' + thumbnail_url
                                if self._is_valid_image_url(url=thumbnail_url):
                                    video_thumbnail_url = thumbnail_url

                            # Video URL
                            matcher = regex.findall(r'"url":"(.+?\.mp4)[^"]*","size"', source, regex.IGNORECASE)
                            if len(matcher) > 0:
                                video_url = matcher[-1]
                                new_video_tag = create_video_tag(src=video_url, thumbnail=video_thumbnail_url,
                                                                 mime_type=self._get_mime_type_from_url(url=video_url))
                                video_tag.insert_before(new_video_tag)
            video_tag.decompose()

        return super()._handle_video(html, default_thumbnail_url, timeout)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    # def _pre_process(self, html):
    #     return super()._pre_process(html)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    # def _post_process(self, html):
    #     return super()._post_process(html)

    def _get_mobile_url(self, url):
        return url.replace('www.nguoiduatin.vn', 'm.nguoiduatin.vn')

    def _get_html(self, url, timeout=15, attempts=3):
        assert url is not None, 'Tham số url không được là None'
        while attempts > 0:
            attempts -= 1
            try:
                headers = {'Referer': self._full_domain}
                response = requests.get(url=url, timeout=timeout, headers=headers,
                                        cookies=self._vars['requests_cookies'],
                                        allow_redirects=False)
                if response.status_code == requests.codes.ok:
                    return response.content.decode('UTF-8')
            except RequestException as e:
                debug(url)
                log(e)
        return None
