#!/usr/bin/python
# -*- coding: utf8 -*-

import bleach
from bs4 import NavigableString

from helpers import *
from normalizer.parser import BaseParser


class SubBaseParser(BaseParser):
    def __init__(self):
        super().__init__()
        # URL ảnh mặc định dùng làm thumbnail cho video khi chưa play
        self._default_video_thumbnail_url = None
        # Mẫu youtube video link
        self._youtube_id_regex = regex.compile(r'(?:youtu\.be|youtube\.com)\/(?:watch\?v=)?([\w-]+)', regex.IGNORECASE)

    # Hàm trả về mobile url nếu có
    def _get_mobile_url(self, url):
        return url

    # Nếu trang có thẻ meta này thì nên dùng vì nó thường chính xác
    def _get_og_title(self, html):
        if html is None:
            return None

        meta_tag = html.find('meta', attrs={'property': 'og:title', 'content': True})
        if meta_tag is None:
            return None

        content = meta_tag.get('content')
        return normalize_string(content) if is_valid_string(content) else None

    # Nếu trang có thẻ meta này thì nên dùng vì nó thường chính xác
    def _get_og_description(self, html):
        if html is None:
            return None

        meta_tag = html.find('meta', attrs={'property': 'og:description', 'content': True})
        if meta_tag is None:
            return None

        content = meta_tag.get('content')
        return normalize_string(content) if is_valid_string(content) else None

    # Nếu trang có thẻ meta này thì nên dùng vì nó thường chính xác
    def _get_og_image(self, html):
        if html is None:
            return None

        meta_tag = html.find('meta', attrs={'property': 'og:image', 'content': True})
        if meta_tag is None:
            return None

        return meta_tag.get('content')

    # Hàm trả về tiêu đề bài viết
    def _get_post_title(self, html):
        if html is None:
            return None

        get_title_tag_func = self._vars.get('get_title_tag_func')
        if get_title_tag_func is None:
            title = self._get_og_title(html=html)
            if title is None:
                return None

            return normalize_string(title) if is_valid_string(title) else None

        title_tag = get_title_tag_func(html)
        if title_tag is None:
            return None

        return normalize_string(title_tag.text) if is_valid_string(title_tag.text) else None

    # Hàm lấy danh sách các keywords có trong thẻ meta
    def _get_meta_keywords(self, html):
        if html is None:
            return None

        meta_tag = html.find('meta', attrs={'name': 'keywords', 'content': True})
        if meta_tag is None:
            return None

        keywords = meta_tag.get('content').split(',')
        normalized_keywords = []
        for keyword in keywords:
            if is_valid_string(keyword):
                normalized_keywords.append(normalize_string(keyword))
        return ', '.join(normalized_keywords)

    # Hàm lấy phần mô tả trong thẻ meta
    def _get_meta_description(self, html):
        if html is None:
            return None

        meta_tag = html.find('meta', attrs={'name': 'description', 'content': True})
        if meta_tag is None:
            return None

        content = meta_tag.get('content')
        return normalize_string(content) if is_valid_string(content) else None

    # Hàm lấy phần mô tả chính
    def _get_summary(self, html):
        if html is None:
            return None

        get_summary_tag_func = self._vars.get('get_summary_tag_func')
        if get_summary_tag_func is None:
            content = self._get_og_description(html=html)
            if content is None:
                return None

            return normalize_string(content) if is_valid_string(content) else None

        summary_tag = get_summary_tag_func(html)
        if summary_tag is None:
            return None

        content = summary_tag.text
        return normalize_string(content) if is_valid_string(content) else None

    # Hàm lấy danh sách keywords
    def _get_tags(self, html):
        if html is None:
            return None

        get_tags_tag_func = self._vars.get('get_tags_tag_func')
        if get_tags_tag_func is None:
            return None

        tags_tag = get_tags_tag_func(html)
        if tags_tag is None:
            return None

        normalized_keywords = []
        for a_tag in tags_tag.find_all('a'):
            keyword = a_tag.text
            if is_valid_string(keyword):
                normalized_keywords.append(normalize_string(keyword))
        return ', '.join(normalized_keywords)

    # Hàm lấy ngày của bài đăng
    def _get_publish_date(self, html):
        if html is None:
            return None

        get_time_tag_func = self._vars.get('get_time_tag_func')
        get_datetime_func = self._vars.get('get_datetime_func')
        if get_time_tag_func is None or get_datetime_func is None:
            return None

        time_tag = get_time_tag_func(html)
        if time_tag is None:
            return None

        return get_datetime_func(normalize_string(time_tag if isinstance(time_tag, str) else time_tag.text))

    # Xử lí các youtube videos có trong bài viết
    def _handle_youtube_video(self, html):
        # Tìm các thẻ div chứa youtube link
        div_tags = html.find_all('div')
        for div_tag in div_tags:
            if len(div_tag.attrs) > 1:
                for value in div_tag.attrs.values():
                    if isinstance(value, str):
                        youtube_id = self._youtube_id_regex.search(value)
                        if youtube_id is not None:
                            video_url = 'https://www.youtube.com/embed/' + youtube_id.group(1)
                            div_tag.replace_with(
                                create_video_tag(src=video_url, width=640, height=360, is_youtube=True))
                            break
        return html

    # Xử lí các videos có trong bài viết
    def _handle_video(self, html, default_thumbnail_url=None, timeout=15):
        # Xử lí tự động link youtube được nhúng vào
        video_tags = html.find_all('iframe', attrs={'src': True, 'height': True})
        for video_tag in video_tags:
            video_url = video_tag.get('src')
            if '.youtu' not in video_url and 'youtube.com' not in video_url:
                continue

            width = video_tag.get('width')
            if width is None:
                width = '100%'

            video_tag.replace_with(
                create_video_tag(src=video_url, width=width, height=video_tag.get('height'),
                                 is_youtube=True))

        return html

    # Xử lí hình ảnh và caption có trong bài viết
    def _handle_image(self, html, title=None):
        if html is None:
            return None

        img_tags = html.find_all('img')
        for img_tag in img_tags:
            image_url = img_tag.get('src')
            image_data_link = img_tag.get('data-link')

            image_url = self._get_valid_image_url(image_url)

            # size = self._get_image_size(url=image_url)
            # if size is None or size[0] < 100 or size[1] < 100:
            #     img_tag.decompose()
            #     continue

            # Tìm thẻ caption
            next_div_tag = img_tag.find_next('div')
            if next_div_tag is not None and next_div_tag.find_parent('main') is not None:
                # Lấy class của thẻ cha
                next_div_classes = next_div_tag.get('class')
                if next_div_classes is None:
                    next_div_classes = []

                # Lấy class của các thẻ con bên trong nó
                child_tags = next_div_tag.find_all(True)
                for child_tag in child_tags:
                    child_tag_classes = child_tag.get('class')
                    if child_tag_classes is not None:
                        next_div_classes.extend(child_tag_classes)

                caption_string = next_div_tag.text

                if regex.search(r'(?:caption|center|italic)', ' '.join(list(set(next_div_classes))),
                                regex.IGNORECASE) is not None or regex.search(r'(?:(?:ảnh|nguồn)[^\n:]{0,20}:)',
                                                                              caption_string,
                                                                              regex.IGNORECASE) is not None:
                    caption_tag = create_caption_tag(caption_string)
                    next_div_tag.replace_with(caption_tag)

            new_img_tag = create_image_tag(url=image_url, alt=title, data_link=image_data_link)
            img_tag.insert_before(new_img_tag)
            img_tag.decompose()

        return html

    # Mỗi đầu báo có thể kế thừa hàm này để xử lí 1 số trường hợp riêng bị như xóa ads,...
    def _pre_process(self, html):
        # Xử lí các thẻ inline chứa image
        inline_tags = html.find_all(['a', 'b', 'i', 'small', 'em', 'strong', 'q', 'span'])
        for inline_tag in inline_tags:
            img_tag = inline_tag.find('img')
            if img_tag is not None:
                inline_tag.name = 'div'
        return html

    # Mỗi đầu báo có thể kế thừa hàm này để xử lí 1 số trường hợp riêng bị như xóa ads,...
    def _post_process(self, html):
        return html

    def _get_special_tag_classes(self, tag):
        if tag is None:
            return []

        classes = tag.get('class')
        if classes is None:
            classes = []
        else:
            caption_classes = self._vars.get('caption_classes')
            if caption_classes is None:
                caption_classes = []

            author_classes = self._vars.get('author_classes')
            if author_classes is None:
                author_classes = []

            caption_classes.extend(['desc', 'pic', 'img', 'box', 'cap', 'photo', 'fig', 'hinh', 'anh', 'def'])
            author_classes.extend(
                ['author', 'copyright', 'source', 'nguon', 'tac-gia', 'tacgia', 'ban-quyen', 'banquyen'])

            caption_classes_regex = regex.compile(r'(?:%s)' % '|'.join(caption_classes), regex.IGNORECASE)
            author_classes_regex = regex.compile(r'(?:%s)' % '|'.join(author_classes), regex.IGNORECASE)

            cls = []

            # Dự đoán nhãn Caption
            if caption_classes_regex.search(' '.join(classes)) is not None:
                cls.append('caption')

            # Dự đoán nhãn Author
            if author_classes_regex.search(' '.join(classes)) is not None:
                cls.append('author')

            classes.extend(cls)

        # Kiểm tra trong align
        align = tag.get('align')
        if align is not None:
            align = align.lower()
            if 'center' in align or 'middle' in align:
                classes.append('center')
            elif 'right' in align:
                classes.append('right')

        # Kiểm tra trong style
        style = tag.get('style')
        if style is not None:
            style = style.lower()
            if 'center' in style or 'middle' in style:
                classes.append('center')
            elif 'right' in style:
                classes.append('right')
            elif 'bold' in style:
                classes.append('bold')

        # Kiểm tra tên thẻ
        if tag.name in ['table', 'td', 'caption', 'figcaption']:
            classes.append('caption')
        elif tag.name in ['strong', 'b']:
            classes.append('bold')
        elif tag.name in ['em', 'i']:
            classes.append('italic')
        elif tag.name in ['center']:
            classes.append('center')

        return list(set(classes))

    @staticmethod
    def _combine_span_tags(span_tag, block_classes=None):
        if span_tag is None or isinstance(span_tag, NavigableString) or span_tag.name != 'span':
            return None

        # Wrap lại bằng div để tránh rời rạc
        span_tag.wrap(create_html_tag('div'))

        parent_span_tag = span_tag.parent

        if block_classes is None:
            block_classes = []

        span_classes = span_tag.get('class')
        if span_classes is None:
            span_classes = []

        span_classes.extend(block_classes)

        s = [(span_tag, list(set(span_classes)))]

        while len(s) > 0:
            tag, classes = s.pop()

            current_tag = tag

            # Lặp qua từng node con
            children = list(tag.children)

            if len(children) > 0:
                temp_tag = create_html_tag('span', attrs={'class': classes} if len(classes) > 0 else {})

                for child_tag in children:
                    if isinstance(child_tag, NavigableString):
                        temp_tag.append(child_tag.extract())
                    else:
                        # Bổ sung thẻ span vào cây nếu có dữ liệu, chỉ nhận thẻ span chứa nội dung có ý nghĩa
                        if len(temp_tag.contents) > 0:
                            # Chèn vào sau thẻ cha
                            current_tag.insert_after(temp_tag)
                            if not is_valid_string(temp_tag.text, r'\s+'):
                                temp_tag.unwrap()

                            current_tag = current_tag.next_sibling
                            temp_tag = create_html_tag('span', attrs={'class': classes} if len(classes) > 0 else {})

                        if child_tag.name == 'br':
                            current_tag.insert_after(child_tag.extract())
                            current_tag = current_tag.next_sibling
                        else:
                            # Lấy thẻ span con ra để khi thẻ cha bị xóa thì không bị xóa theo
                            child_span_tag = child_tag.extract()

                            span_classes = child_tag.get('class')
                            if span_classes is None:
                                span_classes = []

                            span_classes.extend(classes)

                            if len(child_span_tag.contents) > 0:
                                current_tag.insert_after(child_span_tag)
                                current_tag = current_tag.next_sibling
                                s.append((child_span_tag, list(set(span_classes))))
                            else:
                                child_span_tag.decompose()

                # Trường hợp không có tag để đóng lại
                if len(temp_tag.contents) > 0:
                    # Chèn vào sau thẻ cha
                    current_tag.insert_after(temp_tag)
                    if not is_valid_string(temp_tag.text, r'\s+'):
                        temp_tag.unwrap()

            # Xóa thẻ cha vì con của nó đã được đem lên cùng cấp nằm ở phía sau
            tag.decompose()

        return parent_span_tag

    @staticmethod
    def _combine_span_sibling_tags(div_tag):
        if div_tag is None or isinstance(div_tag, NavigableString) or div_tag.name != 'div':
            return None

        children = list(div_tag.children)
        children_size = len(children)

        i = 0
        while i < children_size - 1:
            child_tag = children[i]

            if child_tag.name == 'span':

                j = i + 1
                while j < children_size:
                    next_sibling = children[j]

                    if isinstance(next_sibling, NavigableString):
                        if is_valid_string(str(next_sibling), r'\s+'):
                            break
                        else:
                            # Gộp thẻ span và text gồm các khoảng trắng
                            child_tag.append(next_sibling.extract())
                            i = j
                    else:
                        if next_sibling.name == 'span':
                            # Xử lí gộp hai span kề nhau có chung class
                            child_classes = child_tag.get('class')
                            if child_classes is None:
                                child_classes = []

                            next_sibling_classes = next_sibling.get('class')
                            if next_sibling_classes is None:
                                next_sibling_classes = []

                            if set(child_classes) == set(next_sibling_classes):
                                # Gộp 2 thẻ span
                                child_tag.append(next_sibling.extract())
                                next_sibling.unwrap()
                                i = j
                            else:
                                break
                        else:
                            break
                    j += 1

                # Gộp các string liền kề bên trong span
                child_tag.string = child_tag.text

            i += 1

        # Nếu thẻ div chỉ chứa 1 span thì gộp class của span đó với div bao bên ngoài
        child_tags = div_tag.find_all(True)
        if len(child_tags) == 1 and child_tags[0].name == 'span':
            previous_sibling = all(
                isinstance(sibling, NavigableString) and not is_valid_string(sibling, r'\s+') for sibling in
                child_tags[0].previous_siblings)

            next_sibling = all(
                isinstance(sibling, NavigableString) and not is_valid_string(sibling, r'\s+') for sibling in
                child_tags[0].next_siblings)

            if previous_sibling and next_sibling:
                div_classes = div_tag.get('class')
                if div_classes is None:
                    div_classes = []

                child_classes = child_tags[0].get('class')
                if child_classes is None:
                    child_classes = []

                div_classes.extend(child_classes)
                div_tag.attrs = {'class': list(set(div_classes))}
                child_tags[0].unwrap()

    @staticmethod
    def _combine_div_tags(parent_tag):
        if parent_tag is None or isinstance(parent_tag, NavigableString) or parent_tag.name != 'div':
            return None

        # Clone thẻ div để khi unwrap vẫn không bị mất.
        parent_tag.wrap(create_html_tag('div', attrs=parent_tag.attrs))
        bounding_tag = parent_tag.parent

        classes = parent_tag.get('class')
        s = [(parent_tag, [] if classes is None else classes)]

        while len(s) > 0:
            tag, classes = s.pop()

            # Lặp qua từng node con
            children = list(tag.children)
            children_size = len(children)

            if children_size > 0:
                temp_tag = create_html_tag('div', attrs={'class': classes} if len(classes) > 0 else {})

                i = 0
                while i < children_size:
                    child_tag = children[i]

                    if isinstance(child_tag, NavigableString):
                        temp_tag.append(child_tag.extract())
                    elif child_tag.name == 'span':
                        span_tags = SubBaseParser._combine_span_tags(span_tag=child_tag,
                                                                     block_classes=temp_tag.attrs.get('class'))

                        # Nếu gặp thẻ <br> thì tách ra làm 2 div bởi vì khi nhìn trên browser nó cũng là 2 dòng
                        contents = list(span_tags.children)
                        for child in contents:
                            if child.name == 'br':
                                if len(temp_tag.contents) > 0 and is_valid_string(temp_tag.text, r'\s+'):
                                    span_tags.insert_before(temp_tag)

                                    # Gộp các span anh em có chung class
                                    SubBaseParser._combine_span_sibling_tags(div_tag=temp_tag)

                                    temp_tag = create_html_tag('div',
                                                               attrs={'class': classes} if len(classes) > 0 else {})
                            else:
                                temp_tag.append(child.extract())

                        span_tags.decompose()
                    else:
                        # Bổ sung thẻ div vào cây nếu có dữ liệu, chỉ nhận thẻ div chứa nội dung có ý nghĩa
                        if len(temp_tag.contents) > 0 and is_valid_string(temp_tag.text, r'\s+'):
                            child_tag.insert_before(temp_tag)

                            # Gộp các span anh em có chung class
                            SubBaseParser._combine_span_sibling_tags(div_tag=temp_tag)

                            temp_tag = create_html_tag('div', attrs={'class': classes} if len(classes) > 0 else {})

                        if child_tag.name == 'div':
                            # Thêm vào stack nếu là div
                            child_classes = child_tag.get('class')
                            if child_classes is None:
                                child_classes = []
                            child_classes.extend(classes)
                            if len(child_tag.contents) > 0 and (
                                        is_valid_string(child_tag.text, r'\s+') or child_tag.find(
                                        ['video', 'img']) is not None):
                                s.append((child_tag, list(set(child_classes))))
                            else:
                                child_tag.decompose()
                        else:
                            if child_tag.name not in ['video', 'img']:
                                child_tag.decompose()

                    i += 1

                # Trường hợp không có tag để đóng lại, chỉ nhận thẻ div chứa nội dung có ý nghĩa
                if len(temp_tag.contents) > 0 and is_valid_string(temp_tag.text, r'\s+'):
                    # Đã duyệt qua tất cả thẻ con nên chỉ cần append để vào vị trí cuối
                    tag.append(temp_tag)

                    # Gộp các span anh em có chung class
                    SubBaseParser._combine_span_sibling_tags(div_tag=temp_tag)

                # Xóa thẻ div ngoài cùng nhưng vẫn giữ các thẻ con bên trong nó
                tag.unwrap()
            else:
                # Xóa thẻ div nếu nó không có thẻ con
                tag.decompose()

        return bounding_tag

    def _normalize_content(self, html, title=None, timeout=15):
        if html is None:
            return None

        get_main_content_tag_func = self._vars.get('get_main_content_tag_func')
        if get_main_content_tag_func is None:
            return None

        main_content_tag = get_main_content_tag_func(html)
        if main_content_tag is None:
            return None

        main_content_tag.attrs = {}

        # Xử lí các youtube videos nhúng trong bài viết
        main_content_tag = self._handle_youtube_video(html=main_content_tag)

        # Xử lí thẻ video
        main_content_tag = self._handle_video(html=main_content_tag,
                                              default_thumbnail_url=self._default_video_thumbnail_url, timeout=timeout)

        # Xóa các thẻ không quan trọng
        main_content_tag = remove_tags(html=main_content_tag,
                                       tags=['noscript', 'script', 'canvas', 'embed', 'object', 'param', 'area', 'map',
                                             'track', 'iframe'])

        # Xóa rác
        main_content_tag = self._pre_process(html=main_content_tag)

        # Đổi tên thẻ bao bên ngoài thành main để dễ kiểm soát
        main_content_tag.name = 'main'

        # Chuẩn hóa thẻ
        tags = main_content_tag.find_all(
            ['div', 'p', 'table', 'td', 'caption', 'figcaption', 'center', 'strong', 'b', 'em', 'i'])

        for tag in tags:
            classes = self._get_special_tag_classes(tag=tag)
            tag.name = 'div' if tag.name in ['div', 'p', 'table', 'td', 'caption', 'figcaption', 'center'] else 'span'
            tag.attrs = {'class': classes} if len(classes) > 0 else {}

        attrs = {
            'video': ['width', 'height', 'controls', 'onclick', 'poster', 'youtube', 'data-dummy', 'data-link'],
            'source': ['src', 'type'],
            'img': ['src', 'alt', 'data-link'],
            'div': ['class'],
            'span': ['class']
        }

        filtered_content = bleach.clean(main_content_tag, tags=['main', 'div', 'br', 'video', 'source', 'img', 'span'],
                                        attributes=attrs, strip=True, strip_comments=True)

        filtered_content_tag = get_soup(filtered_content, clear_special_chars=True).main.extract()

        # Xóa bỏ nội dung cũ
        main_content_tag.clear()

        # Thêm dữ liệu đã được lọc vào
        main_content_tag.append(filtered_content_tag)

        # Bỏ thẻ main bao quanh bên ngoài
        filtered_content_tag.unwrap()

        main_content_tag.name = 'div'

        main_content_tag = self._combine_div_tags(parent_tag=main_content_tag)

        main_content_tag.name = 'main'

        # Xử lí thẻ image
        main_content_tag = self._handle_image(html=main_content_tag, title=title)

        # Phục hồi video của youtube
        video_tags = main_content_tag.find_all('video', attrs={'youtube': True})
        for video_tag in video_tags:
            source_tag = video_tag.find('source', attrs={'src': True})
            if source_tag is None:
                video_tag.decompose()
            else:
                new_video_tag = create_youtube_video_tag(src=source_tag.get('src'), width=video_tag.get('width'),
                                                         height=video_tag.get('height'))
                video_tag.replace_with(new_video_tag)

        # Phục hồi lại thuộc tính controls của video
        video_tags = main_content_tag.find_all('video')
        for video_tag in video_tags:
            video_tag['controls'] = None

        main_content_tag = self._post_process(html=main_content_tag)

        return main_content_tag

    def _get_author(self, html):
        if html is None:
            return None

        main_content_tag = html
        html = html.find_parent('html')

        if html is None:
            return None

        get_author_tag_func = self._vars.get('get_author_tag_func')
        if get_author_tag_func is not None:
            author_tag = get_author_tag_func(html)
            authors = []
            if author_tag is not None:
                # Chèn thêm kí tự xuống dòng nếu có thẻ <br/>

                # Xem xét có nên thêm thẻ div và p vào không?
                br_tags = author_tag.find_all('br')
                for br_tag in br_tags:
                    br_tag.insert_after('\r\n')

                lines = regex.split(r'(?:\r?\n)+', author_tag.text)
                for line in lines:
                    if is_valid_string(line):
                        authors.append(normalize_string(line))
            return '\n'.join(authors) if len(authors) > 0 else None

        author_classes_pattern = self._vars.get('author_classes_pattern')
        if author_classes_pattern is None:
            return None

        valid_author_classes = []
        invalid_author_classes = []

        author_classes_patterns = author_classes_pattern.split('|')
        for pattern in author_classes_patterns:
            if pattern.startswith('^'):
                invalid_author_classes.append(pattern[1:])
            else:
                valid_author_classes.append(pattern)

        valid_author_classes_regex = regex.compile(r'(?:%s)' % '|'.join(valid_author_classes), regex.IGNORECASE)
        invalid_author_classes_regex = regex.compile(r'(?:%s)' % '|'.join(invalid_author_classes), regex.IGNORECASE)

        # Tìm tất cả thẻ div ứng viên
        candidate_div_tags = []

        div_tags = main_content_tag.find_all('div')
        div_tags = list(reversed(div_tags))
        for div_tag in div_tags:
            string = normalize_string(div_tag.text)
            # Tên tác giả thường không có dấu .!? ở cuối
            if not is_valid_string(string, r'\s+') or string.endswith('.') \
                    or string.endswith('!') or string.endswith('?'):
                continue

            # Lấy class của thẻ cha
            div_classes = div_tag.get('class')
            if div_classes is None:
                div_classes = []

            # Lấy class của các thẻ con bên trong nó
            child_tags = div_tag.find_all(True)
            for child_tag in child_tags:
                child_tag_classes = child_tag.get('class')
                if child_tag_classes is not None:
                    div_classes.extend(child_tag_classes)

            classes_string = ' '.join(list(set(div_classes)))
            if is_valid_string(classes_string, r'\s+'):
                if len(invalid_author_classes) > 0:
                    if invalid_author_classes_regex.search(classes_string) is not None:
                        continue
                if len(valid_author_classes) > 0:
                    if valid_author_classes_regex.search(classes_string) is not None:
                        candidate_div_tags.append(div_tag)

        candidate_div_tags_size = len(candidate_div_tags)
        if candidate_div_tags_size == 0:
            return None

        authors = [normalize_string(candidate_div_tags[0].text)]

        clear_all_below_author = self._vars.get('clear_all_below_author')
        if clear_all_below_author is not None and clear_all_below_author:
            next_div_tag = candidate_div_tags[0].find_next_sibling(True)
            while next_div_tag is not None:
                current_div_tag = next_div_tag
                next_div_tag = next_div_tag.find_next_sibling(True)
                current_div_tag.decompose()

        # Dò tìm các ứng viên kề nhau
        i = 1
        while i < candidate_div_tags_size:
            if candidate_div_tags[i].find_next_sibling(True) != candidate_div_tags[i - 1]:
                break
            authors.insert(0, normalize_string(candidate_div_tags[i].text))
            candidate_div_tags[i - 1].decompose()
            i += 1

        candidate_div_tags[i - 1].decompose()

        return '\n'.join(authors)

    # Trả về url của ảnh đầu tiên trong content
    def _get_thumbnail(self, html):
        if html is None:
            return None

        main_content_tag = html
        html = html.find_parent('html')
        if html is None:
            return None

        get_thumbnail_url_func = self._vars.get('get_thumbnail_url_func')
        thumbnail_url = self._get_og_image(html=html) if get_thumbnail_url_func is None \
            else get_thumbnail_url_func(html)

        thumbnail_url = thumbnail_url and thumbnail_url.strip()

        if thumbnail_url is None or not self._is_valid_image_url(url=thumbnail_url):
            img_tag = main_content_tag.find('img', attrs={'src': True})
            return None if img_tag is None else img_tag.get('src')

        return self._get_valid_image_url(thumbnail_url)

    # Hàm trả về nội dung theo format yêu cầu
    def _get_content(self, html):
        if html is None:
            return None

        # Unwrap thẻ inline
        tags = html.find_all('span')
        for tag in tags:
            tag.unwrap()

        # Đổi các thẻ div khác sang <p></p> và chuẩn hóa nội dung
        tags = html.find_all('div')
        for tag in tags:
            tag.name = 'p'
            tag.attrs = {}
            normalized_string = normalize_string(tag.text)
            if is_valid_string(string=normalized_string):
                tag.string = normalized_string
            else:
                tag.decompose()

        content = html.decode(formatter=None)
        return regex.sub(r'\s*<\s*\/?\s*main\s*>\s*', '', remove_closing_tags(content=content, tags=['source']))

    # Hàm trả về nội dung đã lọc thẻ html
    def _get_plain(self, html):
        if html is None:
            return None

        lines = []
        tags = html.find_all('p')
        for tag in tags:
            if tag.get('class') is None:
                normalized_string = normalize_string(tag.text)
                if len(normalized_string) > 0 and normalized_string[-1] not in ',.;!?:-':
                    normalized_string += '.'
                lines.append(normalized_string)
        return ' '.join(lines)

    # Hàm chính để gọi các hàm con và tạo kết quả
    def _parse(self, url, html, timeout=15):
        alias = self._get_alias(url=url)
        mobile_url = self._get_mobile_url(url=url)
        post_title = self._get_post_title(html=html)
        meta_keywords = self._get_meta_keywords(html=html)
        meta_description = self._get_meta_description(html=html)

        publish_date = self._get_publish_date(html=html)
        tags = self._get_tags(html=html)
        summary = self._get_summary(html=html)

        normalized_content = self._normalize_content(html=html, title=remove_special_chars(post_title), timeout=timeout)
        author = self._get_author(html=normalized_content)
        thumbnail = self._get_thumbnail(html=normalized_content)
        content = self._get_content(html=normalized_content)
        plain = self._get_plain(html=normalized_content)

        return self._build_json(url=url, mobile_url=mobile_url, title=post_title, alias=alias,
                                meta_keywords=meta_keywords, meta_description=meta_description,
                                publish_date=publish_date, author=author, tags=tags, thumbnail=thumbnail,
                                summary=summary, content=content, plain=plain)
