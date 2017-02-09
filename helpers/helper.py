#!/usr/bin/python
# -*- coding: utf8 -*-
import importlib
import json
import logging
import os
import urllib.request
from inspect import getmembers, isclass
from os.path import splitext
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

import pafy
import regex
import requests
from bs4 import BeautifulSoup

# Đường dẫn tuyệt đối khi mã nguồn được chạy
_APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

# Ghi log
_LOGGER = logging.getLogger(__name__)

# Tạo thẻ html
_BEAUTIFUL_SOUP = BeautifulSoup(features='html5lib')

# Bộ lọc các kí tự đặc biệt
_SPECIAL_CHARS = '“”–'
_NORMAL_CHARS = '""-'
_SPECIAL_CHARS_NORMALIZE_MAP = dict(zip(_SPECIAL_CHARS, _NORMAL_CHARS))
_SPECIAL_CHARS_NORMALIZE_REGEX = regex.compile('|'.join(_SPECIAL_CHARS))

# Rút trích youtube id từ url
_YOUTUBE_ID_REGEX = regex.compile(r'(?:youtu\.be|youtube\.com)\/(?:watch\?v=)?([\w\W]+)', regex.IGNORECASE)


# Hàm ghi log
def log(msg):
    _LOGGER.exception(msg=msg)


# Hàm đổi các kí tự đặc biệt sang kí tự thông thường
def normalize_special_chars(string):
    return _SPECIAL_CHARS_NORMALIZE_REGEX.sub(lambda m: _SPECIAL_CHARS_NORMALIZE_MAP[m.group(0)], string)


# Hàm lọc bỏ các kí tự không cần thiết, các kí tự đặc biệt và các khoảng trắng
def normalize_string(string):
    string = regex.sub(r'\\+(\S)', r'\g<1>', string)
    return regex.sub(r'\s+', ' ', normalize_special_chars(string)).strip()


# Hàm lọc bỏ các kí tự đặc biệt
def remove_special_chars(string):
    return normalize_string(string=regex.sub(r'[\W_]+', ' ', string))


# Kiểm tra một chuỗi có hợp lệ hay không
def is_valid_string(string, pattern=r'[\W_]+'):
    string = regex.sub(pattern, '', string).strip()
    return len(string) > 0


# Định dạng ngày hợp lệ
def format_datetime(obj):
    return obj.strftime('%Y-%m-%d %H:%M:%S')


# Xóa bỏ các tham số có trong url
def clean_url_query(url):
    obj = urlparse(url)
    return '%s://%s%s' % (obj.scheme, obj.netloc, obj.path)


# Kiểm tra image url hợp lệ
def is_valid_image_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.getcode() == 200
    except (HTTPError, URLError):
        pass
    return False


# Lấy Content-Type của url
def get_mime_type_from_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            info = response.info()
            return info.get_content_type()
    except (HTTPError, URLError):
        pass
    return None


# Lấy direct link tạm thời từ youtube
def get_direct_youtube_video(url):
    # Method 1
    """
    youtube_id = _YOUTUBE_ID_REGEX.search(url)
    if youtube_id is None:
        return None
    youtube_id = youtube_id.group(1)
    return 'http://www.youtubeinmp4.com/redirect.php?video=%s' % youtube_id, 'video/mp4'
    """

    # Method 2
    try:
        video = pafy.new(url=url)
        stream = video.getbest(preftype='mp4')
        return stream.url, 'video/mp4'
    except Exception as e:
        log(e)
    return None


# ********** HTML **********


# Tạo thẻ html
def create_html_tag(tag, is_self_closing=False, attrs=None):
    new_tag = BeautifulSoup('<%s>' % tag, features='xml').find(tag) if is_self_closing else _BEAUTIFUL_SOUP.new_tag(tag)
    if attrs is not None:
        new_tag.attrs = attrs
    return new_tag


# Tạo đối tượng BeautifulSoup
def get_soup(string, clear_special_chars=False):
    if clear_special_chars:
        string = regex.sub(r'\s+', ' ', string)
    return BeautifulSoup(string, features='html5lib')


# Tạo thẻ video theo format yêu cầu
def create_video_tag(src, mime_type=None, width=375, height=280, video_tag_name='video', source_tag_name='source'):
    if mime_type is None:
        mime_type = get_mime_type_from_url(url=src)
        if mime_type is None:
            mime_type = 'video/mp4'

    source_tag = create_html_tag(source_tag_name)
    source_tag['src'] = src
    source_tag['type'] = mime_type

    video_tag = create_html_tag(video_tag_name)
    video_tag['width'] = width
    video_tag['height'] = height
    video_tag['controls'] = None
    video_tag.append(source_tag)

    return video_tag


# Tạo thẻ image theo format yêu cầu
def create_image_tag(url, alt, image_tag_name='img'):
    image_tag = create_html_tag(image_tag_name)
    image_tag['src'] = url
    image_tag['alt'] = remove_special_chars(alt)
    return image_tag


# Tạo thẻ caption theo format yêu cầu
def create_caption_tag(string, caption_tag_name='p', class_name='caption'):
    caption_tag = create_html_tag(caption_tag_name)
    caption_tag.attrs = {'class': class_name}
    caption_tag.append(normalize_string(string))
    return caption_tag


# Tải nội dung web
def get_html(url, timeout=15, allow_redirects=False):
    try:
        response = requests.get(url=url, timeout=timeout, allow_redirects=allow_redirects)
        if response.status_code == requests.codes.ok:
            return response.content.decode('UTF-8')
    except Exception as e:
        log(e)
    return None


# *****************************


# ********** FILE IO **********

# Trả về đường dẫn tuyệt đối
def path(*name):
    return os.path.join(_APP_PATH, *name)


# Hàm cho biết đường dẫn cung cấp là tập tin, thư mục hay không tồn tại
def path_info(name):
    if len(name) > 0 and os.path.exists(name):
        if os.path.isfile(name):
            return 1
        if os.path.isdir(name):
            return -1
    return 0


# Hàm tạo thư mục nhiều cấp
def make_dirs(name):
    if len(name) > 0 and path_info(name) >= 0:
        os.makedirs(name)


# Hàm đọc file theo dòng hỗ trợ UTF-8
def read_lines(file_name):
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
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            for line in lines:
                f.write((line + end_line).encode('UTF-8'))
        except Exception as e:
            log(e)


# Hàm đọc file json hỗ trợ UTF-8
def read_json(file_name):
    assert path_info(file_name) == 1, 'File do not exist!'
    with open(file_name, 'rb') as f:
        try:
            return json.loads(f.read().decode('UTF-8'))
        except Exception as e:
            log(e)


# Hàm ghi file json hỗ trợ UTF-8
def write_json(obj, file_name):
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            f.write(json.dumps(obj, indent=4, ensure_ascii=False).encode('UTF-8'))
        except Exception as e:
            log(e)


# Định dạng lại chuỗi json cho dễ nhìn
def prettify_json(obj):
    return json.dumps(obj=obj, indent=4, ensure_ascii=False)


# Hàm trả về danh sách các files có trong thư mục
def read_folder(folder_path, has_extension=True, extension_filter=None):
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
