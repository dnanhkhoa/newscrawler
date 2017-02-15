#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
import importlib
import json
import logging
import os
from datetime import datetime
from inspect import getmembers, isclass
from os.path import splitext
from urllib.parse import urlparse

import pafy
import regex
from bs4 import BeautifulSoup

_APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

# Ghi log
_LOGGER = logging.getLogger(__name__)

# Tạo thẻ html
_BEAUTIFUL_SOUP = BeautifulSoup(features='html5lib')

# Bộ lọc các kí tự đặc biệt
_SPECIAL_CHARS = '“”‘’–\xA0'
_NORMAL_CHARS = '""\'\'- '
_SPECIAL_CHARS_NORMALIZE_MAP = dict(zip(_SPECIAL_CHARS, _NORMAL_CHARS))
_SPECIAL_CHARS_NORMALIZE_REGEX = regex.compile('|'.join(_SPECIAL_CHARS))

# Rút trích youtube id từ url
_YOUTUBE_ID_REGEX = regex.compile(r'(?:youtu\.be|youtube\.com)\/(?:watch\?v=)?([\w\W]+)', regex.IGNORECASE)


# Hàm ghi log
def log(msg):
    _LOGGER.exception(msg=msg)


# Hàm in dữ liệu ra màn hình để DEBUG
def debug(msg):
    print(msg)


# Hàm đổi các kí tự đặc biệt sang kí tự thông thường
def normalize_special_chars(string):
    assert string is not None, 'Tham số string không được là None'
    return _SPECIAL_CHARS_NORMALIZE_REGEX.sub(lambda m: _SPECIAL_CHARS_NORMALIZE_MAP[m.group(0)], string)


# Hàm lọc bỏ các kí tự không cần thiết, các kí tự đặc biệt và các khoảng trắng
def normalize_string(string):
    assert string is not None, 'Tham số string không được là None'
    string = regex.sub(r'\\+(\S)', r'\g<1>', string)
    return regex.sub(r'\s+', ' ', normalize_special_chars(string)).strip()


# Hàm lọc bỏ các kí tự đặc biệt dùng để tạo alt hoặc title
def remove_special_chars(string):
    assert string is not None, 'Tham số string không được là None'
    return normalize_string(string=regex.sub(r'[\W_]+', ' ', string))


# Kiểm tra một chuỗi có hợp lệ hay không, hỗ trợ custom pattern
def is_valid_string(string, pattern=r'[\W_]+'):
    if string is None:
        return False
    string = regex.sub(pattern, '', string).strip()
    return len(string) > 0


# Định dạng ngày hợp lệ theo yêu cầu
def format_datetime(obj):
    assert isinstance(obj, datetime), 'Tham số obj phải là một datetime object'
    return obj.strftime('%Y-%m-%d %H:%M:%S')


# Xóa bỏ các tham số query có trong url
def clean_url_query(url):
    assert url is not None, 'Tham số url không được là None'
    obj = urlparse(url)
    return '%s://%s%s' % (obj.scheme, obj.netloc, obj.path)


# Lấy direct link tạm thời từ youtube
def get_direct_youtube_video(url):
    assert url is not None, 'Tham số url không được là None'

    # Method 1
    # youtube_id = _YOUTUBE_ID_REGEX.search(url)
    # if youtube_id is None:
    #     return None
    # youtube_id = youtube_id.group(1)
    # return 'http://www.youtubeinmp4.com/redirect.php?video=%s' % youtube_id, 'video/mp4'

    # Method 2
    try:
        video = pafy.new(url=url)
        thumbnail_url = video.bigthumb
        if len(thumbnail_url) == 0:
            thumbnail_url = video.thumb
        stream = video.getbest(preftype='mp4')
        return stream.url, thumbnail_url, 'video/mp4'
    except Exception as e:
        log(e)
    return None


# ********** HTML **********

# Tạo thẻ html
def create_html_tag(tag, is_self_closing=False, attrs=None):
    assert tag is not None, 'Tham số tag không được là None'
    new_tag = BeautifulSoup('<%s>' % tag, features='xml').find(tag) if is_self_closing else _BEAUTIFUL_SOUP.new_tag(tag)
    if attrs is not None:
        new_tag.attrs = attrs
    return new_tag


# Tạo đối tượng BeautifulSoup
def get_soup(string, clear_special_chars=False):
    assert string is not None, 'Tham số string không được là None'
    if clear_special_chars:
        string = regex.sub(r'\s+', ' ', string)
    return BeautifulSoup(string, features='html5lib')


# Tạo thẻ video theo format yêu cầu
def create_video_tag(src, thumbnail=None, mime_type=None, width=375, height=280, video_tag_name='video',
                     source_tag_name='source'):
    assert src is not None, 'Tham số src không được là None'

    source_tag = create_html_tag(source_tag_name)
    source_tag['src'] = src
    source_tag['type'] = 'video/mp4' if mime_type is None else mime_type

    video_tag = create_html_tag(video_tag_name)
    video_tag['width'] = width
    video_tag['height'] = height
    video_tag['controls'] = None
    video_tag['onclick'] = 'this.play()'
    video_tag['poster'] = '' if thumbnail is None else thumbnail
    video_tag.append(source_tag)

    return video_tag


# Tạo thẻ image theo format yêu cầu
def create_image_tag(url, alt, image_tag_name='img'):
    assert url is not None, 'Tham số url không được là None'
    image_tag = create_html_tag(image_tag_name)
    image_tag['src'] = url
    image_tag['alt'] = remove_special_chars(alt)
    return image_tag


# Tạo thẻ caption theo format yêu cầu
def create_caption_tag(string, caption_tag_name='p', class_name='caption'):
    assert string is not None, 'Tham số string không được là None'
    caption_tag = create_html_tag(caption_tag_name)
    caption_tag.attrs = {'class': class_name}
    caption_tag.append(normalize_string(string))
    return caption_tag


# Xóa các thẻ đóng không cần thiết
def remove_closing_tags(content, tags):
    assert content is not None, 'Tham số content không được là None'
    if not isinstance(tags, list) or len(tags) == 0:
        return content
    return regex.sub(r'<\s*\/\s*(?:%s)\s*>' % '|'.join(tags), '', content)


# Xóa các thẻ trong danh sách tags
def remove_tags(html, tags):
    assert html is not None, 'Tham số html không được là None'
    for tag in html.find_all(tags):
        tag.decompose()
    return html


# *****************************


# ********** FILE IO **********

# Trả về đường dẫn tuyệt đối
def path(*name):
    assert name is not None, 'Tham số name không được là None'
    return os.path.join(_APP_PATH, *name)


# Hàm cho biết đường dẫn cung cấp là tập tin, thư mục hay không tồn tại
def path_info(name):
    assert name is not None, 'Tham số name không được là None'
    name = path(name)
    if len(name) > 0 and os.path.exists(name):
        if os.path.isfile(name):
            return 1
        if os.path.isdir(name):
            return -1
    return 0


# Hàm tạo thư mục nhiều cấp
def make_dirs(name):
    assert name is not None, 'Tham số name không được là None'
    name = path(name)
    if len(name) > 0 and path_info(name) >= 0:
        os.makedirs(name)


# Hàm đọc file theo dòng hỗ trợ UTF-8
def read_lines(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    lines = []
    with open(file_name, 'rb') as f:
        try:
            for line in f:
                lines.append(line.decode('UTF-8').rstrip('\r\n'))
        except Exception as e:
            log(e)
    return lines


# Hàm ghi file theo dòng hỗ trợ UTF-8
def write_lines(lines, file_name, end_line='\n'):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            for line in lines:
                f.write((line + end_line).encode('UTF-8'))
        except Exception as e:
            log(e)


# Hàm đọc file json hỗ trợ UTF-8
def read_json(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    with open(file_name, 'rb') as f:
        try:
            return json.loads(f.read().decode('UTF-8'))
        except Exception as e:
            log(e)


# Hàm ghi file json hỗ trợ UTF-8
def write_json(obj, file_name):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            f.write(json.dumps(obj, indent=4, ensure_ascii=False).encode('UTF-8'))
        except Exception as e:
            log(e)


# Định dạng lại chuỗi json cho dễ nhìn
def prettify_json(obj):
    assert obj is not None, 'Tham số obj không được là None'
    return json.dumps(obj=obj, indent=4, ensure_ascii=False)


# Hàm trả về danh sách các files có trong thư mục
def read_folder(folder_path, has_extension=True, extension_filter=None):
    folder_path = path(folder_path)
    assert path_info(folder_path) == -1, 'Folder do not exist!'
    files = []
    try:
        for child in os.listdir(folder_path):
            if os.path.isfile('%s/%s' % (folder_path, child)):
                parts = splitext(child)
                if extension_filter is None or parts[1] in extension_filter:
                    files.append(child if has_extension else parts[0])
    except Exception as e:
        log(e)
    return files


# Hàm khởi tạo các đối tượng Parser từ các files trong folder
def create_parser_from_files(folder_path, base_class):
    assert path is not None and base_class is not None, 'Tham số folder_path và base_class không được là None'

    parsers = {}

    files = read_folder(folder_path, has_extension=False, extension_filter=['.py'])
    for file in files:
        module = importlib.import_module('%s.%s' % ('.'.join(folder_path.split('/')), file))
        members = getmembers(module)
        for member in members:
            if isclass(member[1]) and issubclass(member[1], base_class):
                try:
                    instance = member[1]()
                    if instance.get_domain() is None:
                        continue
                    parsers[instance.get_domain()] = instance
                except TypeError:
                    pass
    return parsers

# *****************************
