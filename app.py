#!/usr/bin/python
# -*- coding: utf8 -*-
from normalizer.parser.laodongxahoinet import LaoDongXaHoiNetParser
from utils import *
from normalizer import *

def main():
    bp = LaoDongXaHoiNetParser()
    result = bp.parse('http://laodongxahoi.net/chuong-trinh-tuoi-gia-khong-co-don-trao-qua-tet-cho-cac-cu-cao-nien-o-huyen-soc-son-1305726.html')
    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
