#!/usr/bin/python
# -*- coding: utf8 -*-

import os

os.environ['PAFY_BACKEND'] = 'internal'

from crawler import *
from normalizer import *
from helpers import *


def try_crawler():
    news_crawler = Crawler()

    urls = ['http://giaoducthoidai.vn/khoa-hoc/',
            'http://giaoducthoidai.vn/thoi-su/']
    from_date = '2017-02-10'  # Để None nếu muốn lấy thời gian min hiện tại (%Y-%m-%d 00:00:00)
    to_date = '2017-02-10'  # Để None nếu muốn lấy thời gian max hiện tại (%Y-%m-%d 23:59:59)
    timeout = 15  # Thời gian chờ tối đa

    for url in urls:
        result = news_crawler.crawl(url=url, from_date=from_date, to_date=to_date, timeout=timeout)
        print(result)


def try_normalizer():
    news_normalizer = Normalizer()

    urls = [
        'http://giaoducthoidai.vn/khoa-hoc/laban-key-am-tham-vuon-len-ung-dung-mien-phi-so-1-tren-ios-2903278-l.html',
        'http://giaoducthoidai.vn/khoa-hoc/sinh-vat-giong-nguoi-tuyet-trong-rung-ukraine-2903321-l.html',
        'http://giaoducthoidai.vn/giao-duc/ra-mat-quy-hoa-sen-co-vu-tinh-than-dh-khong-vi-loi-nhuan-2909850-v.html',
        'http://giaoducthoidai.vn/thoi-su/nghin-nguoi-muot-mo-hoi-doi-nang-cau-an-chua-ba-thien-hau-2908215-l.html',
        'http://giaoducthoidai.vn/khoa-hoc/ho-mang-chua-khong-lo-cui-dau-khuat-phuc-ban-tay-tho-san-2909122-l.html'
    ]

    result = news_normalizer.normalize(url=urls[4], timeout=15)
    print(json.dumps(result, indent=4, ensure_ascii=False))


def main():
    # try_crawler()
    try_normalizer()
    return

if __name__ == '__main__':
    main()
