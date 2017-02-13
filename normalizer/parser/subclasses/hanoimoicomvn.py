#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from normalizer.parser import *


class HaNoiMoiComVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Tên trang web sử dụng kiểu Title Case
        self._source_page = 'Hà Nội Mới'

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'hanoimoi.com.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://hanoimoi.com.vn'

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
        def get_tags_tag_func(html):
            div_tag = html.find('div', class_='tagbox')
            if div_tag is None:
                return None
            div_tags = div_tag.find_all('div', class_='tags')
            return div_tags[-1] if len(div_tags) > 0 else None

        self._vars['get_tags_tag_func'] = get_tags_tag_func

        # Tìm thẻ chứa chuỗi thời gian đăng bài
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            div_tags = html.find_all('div', class_='refer')
            if len(div_tags) == 0:
                return None

            a_tag = div_tags[-1].find('a', class_='cap')
            if a_tag is not None:
                a_tag.decompose()

            return div_tags[-1]

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Định dạng chuỗi thời gian và trả về đối tượng datetime
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            time_matcher = regex.search(r'(\d{2}:\d{2})', string, regex.IGNORECASE)
            date_matcher = regex.search(r'(\d{2}\/\d{2}\/\d{4})', string, regex.IGNORECASE)
            if time_matcher is None or date_matcher is None:
                return None
            return datetime.strptime('%s %s' % (date_matcher.group(1), time_matcher.group(1)), '%d/%m/%Y %H:%M')

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
        def get_main_content_tag_func(html):
            div_tag = html.find('div', id='NewsGallery')
            if div_tag is None:
                div_tag = html.find('div', class_='summ')
            return div_tag

        self._vars['get_main_content_tag_func'] = get_main_content_tag_func

        # Chỉ định thẻ chứa tên tác giả
        # Khi sử dụng thẻ này thì sẽ tự động không sử dụng tính năng tự động nhận dạng tên tác giả
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_author_tag_func'] =

        # Chỉ định các nhãn được phép và không được phép dùng để dự đoán author
        # Các nhãn: author, center, right, bold, italic
        # Phân cách nhau bởi dấu | và những nhãn nào không được phép thì có tiền tố ^ ở đầu
        # Ví dụ: 'right|bold|author|^center|^italic'
        self._vars['author_classes_pattern'] = 'author'

        # Trả về url chứa hình ảnh thumbnail được lưu ở thẻ bên ngoài nội dung chính
        # Mặc định sẽ tự động nhận dạng
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_thumbnail_url_func'] =

    # Hàm xử lí video có trong bài, tùy mỗi player mà có cách xử lí khác nhau
    # Khi xử lí xong cần thay thế thẻ đó thành thẻ video theo format qui định
    # Nếu cần tìm link trực tiếp của video trên youtube thì trong helper có hàm hỗ trợ
    def _handle_video(self, html, timeout=15):
        video_regex = regex.compile(r"file: '([^']+)'", regex.IGNORECASE)
        html_tag = html.find_parent('html')
        if html_tag is not None:
            script_tags = html_tag.find_all('script')
            for script_tag in script_tags:
                matcher = video_regex.search(script_tag.text)
                if matcher is not None:
                    video_url = matcher.group(1)
                    if 'youtu' in video_url:
                        video_url, mine_type = get_direct_youtube_video(video_url)
                    else:
                        mine_type = self._get_mime_type_from_url(url=video_url)
                    video_tag = create_video_tag(src=video_url, mime_type=mine_type)
                    html.insert(0, video_tag)
                script_tag.decompose()
        return html

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _pre_process(self, html):
        tag = html.find('div', class_='tagbox')
        if tag is not None:
            tag.decompose()
        return super()._pre_process(html)

    # Sử dụng khi muốn xóa phần tử nào đó trên trang để việc parse được thuận tiện
    def _post_process(self, html):
        div_tag = html.find('div', attrs={'class': 'bold'})
        if div_tag is not None:
            div_tag.decompose()
        return html

    def _get_author(self, html):
        author = super()._get_author(html)
        if author is None:
            html_tag = html.find_parent('html')
            if html_tag is not None:
                author_tag = html_tag.find('div', class_='author')
                if author_tag is not None:
                    author = normalize_string(author_tag.text)
        return author

    def _get_html(self, url, timeout=15, attempts=3):
        assert url is not None, 'Tham số url không được là None'
        while attempts > 0:
            try:
                response = requests.get(url=url, timeout=timeout, allow_redirects=True)
                if response.status_code == requests.codes.ok:
                    return response.content.decode('UTF-8')
            except RequestException as e:
                log(e)
            attempts -= 1
        return None
