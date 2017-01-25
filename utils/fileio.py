#!/usr/bin/python
# -*- coding: utf8 -*-
import importlib
import json
import logging
import os
from inspect import getmembers, isclass
from os.path import splitext

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

_logger = logging.getLogger(__name__)

"""
Hàm tạo đường dẫn tuyệt đối
"""


def path(*name):
    return os.path.join(APP_PATH, *name)


"""
Hàm cho biết đường dẫn cung cấp là tập tin, thư mục hay là không tồn tại
"""


def path_info(name):
    if os.path.exists(name):
        if os.path.isfile(name):
            return 1
        if os.path.isdir(name):
            return -1
    return 0


"""
Hàm tạo thư mục nhiều cấp
"""


def make_dirs(name):
    if len(name) > 0 and path_info(name) >= 0:
        os.makedirs(name)


"""
Hàm đọc file theo dòng hỗ trợ UTF-8
"""


def read_lines(file_name):
    assert os.path.exists(file_name), 'File does not exist!'
    lines = []
    with open(file_name, 'rb') as f:
        try:
            for line in f:
                lines.append(line.decode('UTF-8').rstrip('\r\n'))
        except Exception as e:
            _logger.exception(e)
    return lines


"""
Hàm ghi file theo dòng hỗ trợ UTF-8
"""


def write_lines(lines, file_name, end_line='\n'):
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            for line in lines:
                f.write((line + end_line).encode('UTF-8'))
        except Exception as e:
            _logger.exception(e)


"""
Hàm đọc file json hỗ trợ UTF-8
"""


def read_json(file_name):
    assert os.path.exists(file_name), 'File does not exist!'
    with open(file_name, 'rb') as f:
        try:
            return json.loads(f.read().decode('UTF-8'))
        except Exception as e:
            _logger.exception(e)


"""
Hàm ghi file json hỗ trợ UTF-8
"""


def write_json(obj, file_name):
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            f.write(json.dumps(obj, ensure_ascii=False).encode('UTF-8'))
        except Exception as e:
            _logger.exception(e)


"""
Hàm trả về danh sách các files có trong thư mục
"""


def read_folder(folder_path, has_extension=True, extension_filter=None):
    assert path_info(folder_path) == -1, 'Folder does not exist!'
    files = []
    try:
        for child in os.listdir(folder_path):
            if os.path.isfile('%s/%s' % (folder_path, child)):
                parts = splitext(child)
                if extension_filter is None or parts[1] in extension_filter:
                    files.append(child if has_extension else parts[0])
    except Exception as e:
        _logger.exception(e)
    return files


"""
Hàm khởi tạo các đối tượng Parser từ các files trong folder
"""


def create_parser_from_files(folder_path, base_class):
    parsers = {}
    files = read_folder(folder_path, has_extension=False, extension_filter=['.py'])
    for file in files:
        module = importlib.import_module('%s.%s' % ('.'.join(folder_path.split('/')), file))
        members = getmembers(module)
        for member in members:
            if isclass(member[1]) and issubclass(member[1], base_class) and member[1] is not base_class:
                instance = member[1]()
                parsers[instance._domain] = instance
    return parsers
