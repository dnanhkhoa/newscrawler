#!/usr/bin/python
# -*- coding: utf8 -*-

import os

os.environ['PAFY_BACKEND'] = 'internal'

from crawler import *
from normalizer import *
from helpers import *


def try_crawler():
    news_crawler = Crawler()

    # urls = [
    #     'http://baochinhphu.vn/Doi-song/302.vgp',
    #     'http://baochinhphu.vn/Du-lich/448.vgp',
    #     'http://baochinhphu.vn/Giao-duc/452.vgp',
    #     'http://baochinhphu.vn/Khoa-hoc-Cong-nghe/8.vgp',
    #     'http://baochinhphu.vn/Kinh-te/7.vgp',
    #     'http://baochinhphu.vn/Phap-luat/29.vgp',
    #     'http://baochinhphu.vn/Quoc-te/6.vgp',
    #     'http://baochinhphu.vn/The-thao/447.vgp'
    # ]

    # urls = [
    #     "http://baodatviet.vn/chinh-tri-xa-hoi/giao-duc/",
    #     "http://baodatviet.vn/chinh-tri-xa-hoi/tin-tuc-thoi-su/",
    #     "http://baodatviet.vn/khoa-hoc/",
    #     "http://baodatviet.vn/kinh-te/",
    #     "http://baodatviet.vn/the-gioi/",
    #     "http://baodatviet.vn/the-thao/"
    # ]

    # urls = [
    #     'http://baoquocte.vn/khoa-hoc-cong-nghe',
    #     'http://baoquocte.vn/kinh-te',
    #     'http://baoquocte.vn/the-gioi',
    #     'http://baoquocte.vn/the-thao',
    #     'http://baoquocte.vn/xa-hoi/doi-song-suc-khoe',
    #     'http://baoquocte.vn/xa-hoi/giao-duc'
    # ]

    # urls = [
    #     'http://www.nss.vn/c2-san-pham.htm',
    #     'http://www.nss.vn/c21-kinh-doanh.htm',
    #     'http://www.nss.vn/c116-ngan-hang-so.htm',
    #     'http://www.nss.vn/c100-bao-mat.htm',
    #     'http://www.nss.vn/c18-song-online.htm',
    #     'http://www.nss.vn/c27-game.htm',
    #     'http://www.nss.vn/c115-cong-nghe-xanh.htm'
    # ]

    # urls = [
    #     'http://ione.vnexpress.net/tin-tuc/lam-dep',
    #     'http://ione.vnexpress.net/tin-tuc/phim',
    #     'http://ione.vnexpress.net/tin-tuc/sao',
    #     'http://ione.vnexpress.net/tin-tuc/thoi-trang'
    # ]

    urls = [
        'http://hanoimoi.com.vn/Danh-muc-tin/100/Khoa-hoc',
        'http://hanoimoi.com.vn/Danh-muc-tin/163/Xa-hoi',
        'http://hanoimoi.com.vn/Danh-muc-tin/164/Giao-duc',
        'http://hanoimoi.com.vn/Danh-muc-tin/166/Du-lich',
        'http://hanoimoi.com.vn/Danh-muc-tin/170/The-thao',
        'http://hanoimoi.com.vn/Danh-muc-tin/175/Phap-luat',
        'http://hanoimoi.com.vn/Danh-muc-tin/189/The-gioi',
        'http://hanoimoi.com.vn/Danh-muc-tin/190/Kinh-te',
        'http://hanoimoi.com.vn/Danh-muc-tin/191/Thoi-trang',
        'http://hanoimoi.com.vn/Danh-muc-tin/601/Oto-xemay',
        'http://hanoimoi.com.vn/Danh-muc-tin/741/Hau-truong'
    ]

    from_date = '2017-02-05'  # Để None nếu muốn lấy thời gian min hiện tại (%Y-%m-%d 00:00:00)
    to_date = '2017-02-12'  # Để None nếu muốn lấy thời gian max hiện tại (%Y-%m-%d 23:59:59)
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

    result = news_normalizer.normalize(url=urls[1], timeout=15)
    print(json.dumps(result, indent=4, ensure_ascii=False))


def main():
    try_crawler()
    #try_normalizer()
    return

if __name__ == '__main__':
    main()
