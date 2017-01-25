#!/usr/bin/python
# -*- coding: utf8 -*-
from crawler import *
from normalizer import *
from utils import *


def main():
    link = [
        'http://laodongxahoi.net/chuong-trinh-tuoi-gia-khong-co-don-trao-qua-tet-cho-cac-cu-cao-nien-o-huyen-soc-son-1305726.html',
        'http://laodongxahoi.net/bo-truong-dao-ngoc-dung-gap-mat-chuc-tet-can-bo-huu-tri-nhan-dip-xuan-dinh-dau-2017-1305713.html',
        'http://laodongxahoi.net/gap-mat-cac-can-bo-huu-tri-tai-phia-nam-1305712.html',
        'http://laodongxahoi.net/nga-chan-hon-900-phan-tu-khung-bo-am-muu-xam-nhap-lanh-tho-1305678.html'
    ]
    crawler = Crawler()
    normalizer = Normalizer()
    result = normalizer.normalize(link[2])
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
