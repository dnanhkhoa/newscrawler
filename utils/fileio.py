#!/usr/bin/python
# -*- coding: utf8 -*-
import json
import logging
import os

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
