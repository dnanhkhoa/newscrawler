#!/usr/bin/python
# -*- coding: utf8 -*-

import os

os.environ['PAFY_BACKEND'] = 'internal'

from crawler import *
from normalizer import *
from checker import *


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
    #     'http://www.nss.vn/c66-su-kien.htm',
    #     'http://www.nss.vn/c2-san-pham.htm',
    #     'http://www.nss.vn/c21-kinh-doanh.htm',
    #     'http://www.nss.vn/c116-ngan-hang-so.htm',
    #     'http://www.nss.vn/c100-bao-mat.htm',
    #     'http://www.nss.vn/c18-song-online.htm',
    #     'http://www.nss.vn/c27-game.htm',
    #     'http://www.nss.vn/c115-cong-nghe-xanh.htm',
    #     'http://www.nss.vn/c6-nhan-luc.htm',
    # ]

    # urls = [
    #     'http://ione.vnexpress.net/tin-tuc/lam-dep',
    #     'http://ione.vnexpress.net/tin-tuc/phim',
    #     'http://ione.vnexpress.net/tin-tuc/sao',
    #     'http://ione.vnexpress.net/tin-tuc/thoi-trang'
    # ]

    # urls = [
    #     'http://hanoimoi.com.vn/Danh-muc-tin/100/Khoa-hoc',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/163/Xa-hoi',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/164/Giao-duc',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/166/Du-lich',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/170/The-thao',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/175/Phap-luat',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/189/The-gioi',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/190/Kinh-te',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/191/Thoi-trang',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/601/Oto-xemay',
    #     'http://hanoimoi.com.vn/Danh-muc-tin/741/Hau-truong'
    # ]

    # urls = [
    #     'http://nongnghiep.vn/phap-luat-15-15.html',
    #     'http://nongnghiep.vn/van-hoa-86-15.html',
    #     'http://nongnghiep.vn/the-gioi-8-15.html',
    #     'http://nongnghiep.vn/kinh-te-3-15.html',
    #     'http://nongnghiep.vn/giao-duc-84-15.html',
    #     'http://nongnghiep.vn/the-thao-90-15.html',
    #     'http://nongnghiep.vn/giai-tri-87-15.html'
    # ]

    # urls = [
    #     'http://giaoducthoidai.vn/kinh-te-xa-hoi/',
    #     'http://giaoducthoidai.vn/phap-luat/',
    #     'http://giaoducthoidai.vn/the-gioi/',
    #     'http://giaoducthoidai.vn/kinh-te-xa-hoi/',
    #     'http://giaoducthoidai.vn/giao-duc/',
    #     'http://giaoducthoidai.vn/the-gioi-sao/',
    #     'http://giaoducthoidai.vn/khoa-hoc/',
    #     'http://giaoducthoidai.vn/lam-dep/'
    # ]

    # urls = [
    #     'http://infogame.vn/thong-tin.html',
    #     'http://infogame.vn/chuyen-dong-game.html',
    #     'http://infogame.vn/cong-dong.html',
    #     'http://infogame.vn/anh-video.html'
    # ]

    # urls = [
    #     'http://ngoisao.net/tin-tuc/thoi-cuoc/24h',
    #     'http://ngoisao.net/tin-tuc/thoi-cuoc/thuong-truong',
    #     'http://ngoisao.net/tin-tuc/hau-truong/showbiz-viet',
    #     'http://ngoisao.net/tin-tuc/hau-truong/chau-a',
    #     'http://ngoisao.net/tin-tuc/hau-truong/hollywood',
    #     'http://ngoisao.net/tin-tuc/an-choi/choi-dau',
    #     'http://ngoisao.net/tin-tuc/dan-choi',
    #     'http://ngoisao.net/tin-tuc/lam-dep/sao-dep',
    #     'http://ngoisao.net/tin-tuc/lam-dep/bi-quyet',
    #     'http://ngoisao.net/tin-tuc/thoi-trang/xu-huong',
    #     'http://ngoisao.net/tin-tuc/thoi-trang/sao-style',
    #     'http://ngoisao.net/tin-tuc/thoi-trang/tu-van',
    #     'http://ngoisao.net/tin-tuc/an-choi/an-gi'
    # ]

    # urls = [
    #     'https://cafeland.vn/quy-hoach/',
    #     'https://cafeland.vn/tin-tuc/'
    # ]

    # urls = [
    #     'http://viettimes.vn/bat-dong-san/',
    #     'http://viettimes.vn/du-lich/',
    #     'http://viettimes.vn/giai-tri/',
    #     'http://viettimes.vn/kinh-doanh/',
    #     'http://viettimes.vn/nhip-song-so/',
    #     'http://viettimes.vn/quoc-phong/',
    #     'http://viettimes.vn/song-xanh/',
    #     'http://viettimes.vn/the-gioi/',
    #     'http://viettimes.vn/viet-nam/'
    # ]

    # urls = [
    # 'http://tapchithoitrangtre.com.vn/chan-dung/showbiz',
    # 'http://tapchithoitrangtre.com.vn/chan-dung/sao-quoc-te',
    # 'http://tapchithoitrangtre.com.vn/chan-dung/tro-chuyen-cung-sao',
    #
    # 'http://tapchithoitrangtre.com.vn/phong-cach/lam-dep',
    # 'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang',
    # 'http://tapchithoitrangtre.com.vn/phong-cach/ket-hop',

    # 'http://tapchithoitrangtre.com.vn/song-khoe/dac-quyen-phai-dep',
    # 'http://tapchithoitrangtre.com.vn/song-khoe/dinh-duong',
    # 'http://tapchithoitrangtre.com.vn/song-khoe/dai-lo-nhan-sac',
    # 'http://tapchithoitrangtre.com.vn/song-khoe/suc-khoe'
    # ]

    # urls = [
    #     'https://www.techcombank.com.vn/khach-hang-ca-nhan/chuong-trinh-uu-dai/khuyen-mai-cho-san-pham'
    # ]

    # urls = [
    #     'http://ngoisao.net/tin-tuc/trac-nghiem',
    #     'http://ione.vnexpress.net/tin-tuc/chiem-tinh'
    # ]

    urls = ['http://tapchithoitrangtre.com.vn/song-khoe/suc-khoe']

    from_date = '2017-04-23'  # Để None nếu muốn lấy thời gian min hiện tại (%Y-%m-%d 00:00:00)
    to_date = None  # Để None nếu muốn lấy thời gian max hiện tại (%Y-%m-%d 23:59:59)
    timeout = 15  # Thời gian chờ tối đa

    for url in urls:
        result = news_crawler.crawl(url=url, from_date=from_date, to_date=to_date, timeout=timeout)
        if not result.is_ok():
            continue
        content = result.get_content()
        print(len(content), content)


def try_normalizer():
    news_normalizer = Normalizer()

    # urls = [
    #     'http://giaoducthoidai.vn/khoa-hoc/laban-key-am-tham-vuon-len-ung-dung-mien-phi-so-1-tren-ios-2903278-l.html',
    #     'http://giaoducthoidai.vn/khoa-hoc/sinh-vat-giong-nguoi-tuyet-trong-rung-ukraine-2903321-l.html',
    #     'http://giaoducthoidai.vn/giao-duc/ra-mat-quy-hoa-sen-co-vu-tinh-than-dh-khong-vi-loi-nhuan-2909850-v.html',
    #     'http://giaoducthoidai.vn/thoi-su/nghin-nguoi-muot-mo-hoi-doi-nang-cau-an-chua-ba-thien-hau-2908215-l.html',
    #     'http://giaoducthoidai.vn/khoa-hoc/ho-mang-chua-khong-lo-cui-dau-khuat-phuc-ban-tay-tho-san-2909122-l.html'
    # ]

    # urls = [
    #     'http://baochinhphu.vn/Chuyen-hoi-nhap/Tom-xuat-vao-Han-Quoc-phai-chi-dinh-kiem-dich-tu-14/298649.vgp',
    #     'http://baochinhphu.vn/Hoat-dong-cua-lanh-dao-Dang-Nha-nuoc/Thu-tuong-Bac-Ninh-can-huong-toi-la-mot-trong-nhung-thanh-pho-sang-tao-nhat/298516.vgp',
    #     'http://baochinhphu.vn/The-thao/Van-dong-vien-huan-luyen-vien-xuat-sac-duoc-huong-che-do-cao/298419.vgp',
    #     'http://baochinhphu.vn/Cac-bai-phat-bieu-cua-Thu-tuong/Chinh-phu-kien-tao-va-hanh-dong-dong-luc-moi-cho-phat-trien/295394.vgp',
    #     'http://baochinhphu.vn/Van-hoa/Yen-Tu-ngay-Hoi-xuan/298478.vgp',
    #     'http://baochinhphu.vn/APEC-2017/APEC-phai-khang-dinh-vai-tro-dien-dan-kinh-te-hang-dau/293647.vgp'
    # ]

    # urls = [
    #     'http://baodatviet.vn/the-gioi/quan-he-quoc-te/ai-chi-tien-ban-cho-hacker-nga-pha-hoai-nha-nuoc-nga-3328984/',
    #     'http://baodatviet.vn/the-gioi/tin-tuc-24h/bao-nhat-bien-dong-nhan-su-cap-cao-trung-quoc-3328980/',
    #     'http://baodatviet.vn/kinh-te/dai-gia/the-gioi-choang-voi-du-thuyen-9900-ty-3328994/',
    #     'http://baodatviet.vn/kinh-te/tai-chinh/dong-nhan-dan-te-yeu-den-luc-trung-quoc-phai-so-3328852/',
    #     'http://baodatviet.vn/quoc-phong/vu-khi/my-chi-nguyen-nhan-khien-nga-chua-the-trang-bi-t-50-3328904/',
    #     'http://baodatviet.vn/anh-nong/minuteman-3-nam-ngoai-kha-nang-danh-chan-cua-nga-3328897/'
    # ]

    # urls = [
    #     'http://baoquocte.vn/dang-co-hien-tuong-tham-nhung-ve-tam-linh-44131.html',
    #     'http://baoquocte.vn/cac-cong-dan-the-ky-21-nen-biet-ro-nhung-dieu-gi-43623.html',
    #     'http://baoquocte.vn/ba-con-viet-kieu-tai-bi-gap-mat-mung-xuan-dinh-dau-ha-noi-44130.html',
    #     'http://baoquocte.vn/linh-thieng-le-khai-an-den-tran-xuan-dinh-dau-2017-44085.html',
    #     'http://baoquocte.vn/cung-ngam-cu-da-phat-co-1-khong-2-cua-messi-43733.html',
    #     'http://baoquocte.vn/ve-dep-cuon-hut-cua-de-nhat-phu-nhan-my-43888.html'
    # ]

    # urls = [
    #     'http://hanoimoi.com.vn/Tin-tuc/Gia-dinh/850218/video-mach-ban-lam-vuon-rau-sach-trong-can-bep-nho',
    #     'http://hanoimoi.com.vn/Media/Chuyen-la/845406/video-co-gai-bi-tum-toc-keo-le-ma-khong-ai-cuu-gay-chu-y-tuan-qua',
    #     'http://hanoimoi.com.vn/Tin-tuc/Chinh-tri/862286/chu-tich-nuoc-du-le-khanh-thanh-den-tho-vua-mai-hac-de',
    #     'http://hanoimoi.com.vn/Tin-tuc/Gioi-tre/862203/thanh-nien-thu-do-san-sang-nhap-ngu',
    #     'http://hanoimoi.com.vn/Tin-tuc/Ngoai-hang-Anh/862291/cuu-danh-thu-ha-lan-qua-doi-o-tuoi-73',
    #     'http://hanoimoi.com.vn/Tin-tuc/Cong-nghe/862276/the-he-chip-intel-core-thu-8-se-khong-thuc-su-vuot-troi',
    #     'http://hanoimoi.com.vn/Media/Du-lich/862131/cafe-sua-da-viet-nam-lot-danh-sach-nhung-coc-cafe-ngon-nhat-the-gioi',
    #     'http://hanoimoi.com.vn/Media/Chinh-tri/862233/thuong-truc-thanh-uy-ha-noi-gap-mat-cac-hoi-vien-clb-thang-long'
    # ]
    #
    # urls = [
    #     'http://ione.vnexpress.net/tin-tuc/sao/us-uk/video-hot-nhat-the-gioi-2016-adele-hat-tren-xe-3511046.html',
    #     'http://ione.vnexpress.net/tin-tuc/thoi-trang/bo-anh-mac-vay-to-son-loe-loet-cua-mau-nam-next-top-gay-tranh-cai-3539779.html'
    #     'http://ione.vnexpress.net/tin-tuc/lam-dep/co-gai-makeup-xinh-dep-bang-do-an-trong-tu-lanh-3509827.html',
    #     'http://ione.vnexpress.net/tin-tuc/nhip-song/nhung-kiet-tac-rong-co-the-khien-rong-hai-phong-chao-thua-3528937.html',
    #     'http://ione.vnexpress.net/tin-tuc/sao/viet-nam/co-gai-nguoi-han-hat-hit-big-bang-tai-giong-hat-viet-gay-phan-khich-3540185.html',
    #     'http://ione.vnexpress.net/tin-tuc/lam-dep/dang-dep/mau-noi-y-xu-han-mat-ngay-tho-body-boc-lua-3540144.html',
    #     'http://ione.vnexpress.net/photo/thoi-trang/con-gai-donald-trump-sanh-dieu-so-voi-20-nam-truoc-3539813.html',
    #     'http://ione.vnexpress.net/tin-tuc/sao/chau-a/tzuyu-kiem-duoc-36-ty-dong-sau-hon-mot-nam-debut-3512802.html',
    # ]

    # urls = ['http://nongnghiep.vn/kiem-tra-doanh-nghiep-trung-quoc-quyt-tien-danh-ba-bau-post192325.html',
    #         'http://nongnghiep.vn/vu-vinh-phuc-ha-sat-nan-nhan-xong-hung-thu-nhan-tin-bao-cong-an-noi-giau-xac-post192264.html',
    #         'http://nongnghiep.vn/ten-cuop-tiem-vang-dien-cuong-na-dan-vao-3-canh-sat-post192251.html',
    #         'http://nongnghiep.vn/dang-dieu-tra-lam-ro-don-to-cao-nhom-nguoi-la-dung-sung-de-doa-chu-nha-nghi-viet-thanh-post192270.html',
    #         'http://nongnghiep.vn/tron-truy-na-21-nam-ra-dau-thu-duoc-dinh-chi-vu-an-post192207.html',
    #         'http://nongnghiep.vn/ten-cuop-tiem-vang-dien-cuong-na-dan-vao-3-canh-sat-post192251.html',
    #         'http://nongnghiep.vn/thu-tuc-dang-ky-khai-sinh-cho-tre-bi-bo-roi-post192192.html',
    #         'http://nongnghiep.vn/rung-dong-chong-ho-sat-hai-me-vo-bat-coc-con-trai-nguoi-tinh-post192236.html',
    #         'http://nongnghiep.vn/bat-nguyen-pho-tong-giam-doc-donga-bank-post192202.html',
    #         'http://nongnghiep.vn/bat-qua-tang-12-doi-tuong-danh-bac-thu-giu-142-trieu-dong-post192198.html',
    #         'http://nongnghiep.vn/bat-qua-tang-12-doi-tuong-to-chuc-danh-bac-trong-quan-caphe-post192177.html'
    #         ]

    # urls = [
    #     'http://www.nss.vn/ca2-n35240-video-dung-oc-sen-de-ve-sinh-iphone-7.htm',
    #     'http://www.nss.vn/ca2-n35998-video-lg-g6-chiec-smartphone-hoan-hao.htm',
    #     'http://www.nss.vn/ca21-n36363-doanh-so-smartphone-toan-cau-nam-2016-dat-gan-15-ti-chiec.htm',
    #     'http://www.nss.vn/ca100-n36365-hang-trieu-tai-khoan-twitter-duoc-dang-ky-tai-viet-nam-bi-rao-ban.htm',
    #     'http://www.nss.vn/ca113-n36350-khach-du-lich-se-duoc-trai-nghiem-taxi-drone-o-dubai.htm',
    #     'http://www.nss.vn/ca27-n36361-niantic-da-chuan-bi-tung-ra-mot-ban-cap-nhat-moi-cho-tua-game-pokemon-go.htm',
    #     'http://www.nss.vn/ca27-n36298-google-danh-tang-mini-game-valentine-cho-te-te.htm'
    # ]

    # urls = [
    #     'http://infogame.vn/game-online/kho-do-voi-clip-so-sanh-gai-xinh-gai-xau-cua-vtc-game-14779.html',
    #     'http://infogame.vn/cong-nghe/facebook-cho-dang-bai-news-feed-nhung-an-tren-timeline-41533.html',
    #     'http://infogame.vn/game-mobile/hac-dieu-va-nhung-dai-gia-mot-thoi-trong-vo-lam-truyen-ky-36372.html',
    #     'http://infogame.vn/video/top-nhung-pha-tau-thoat-kinh-dien-tai-cktg-2016-40900.html',
    #     'http://infogame.vn/game-mobile/vtc-game-xac-nhan-phat-hanh-thien-tu-3d-game-quoc-chien-moi-cua-snail-games-42776.html',
    #     'http://infogame.vn/game-mobile/soi-do-khung-cua-nhan-vat-dang-manh-nhat-vo-lam-truyen-ky-mobile-42342.html',
    #     'http://infogame.vn/cong-nghe/video-clip-tren-tay-sung-thuc-te-ao-made-in-vietnam-16130.html'
    # ]

    # urls =[
    #     'http://ngoisao.net/tin-tuc/an-choi/an-gi/10-dung-cu-lam-bep-khien-ban-tron-mat-ngac-nhien-3565511.html'
    # ]

    # urls = [
    #     'http://viettimes.vn/vu-mat-20000-usd-de-xuat-khau-gao-co-the-xu-ly-hinh-su-neu-phat-hien-sai-pham-110215.html',
    #     'http://viettimes.vn/thanh-tra-chinh-phu-kien-nghi-xu-ly-hinh-su-du-an-dai-thanh-cua-dai-gia-dieu-cay-110846.html',
    #     'http://viettimes.vn/vietlott-mo-thang-3-bang-giai-jackpot-412-ty-110974.html',
    #     'http://viettimes.vn/video-trai-nghiem-nhanh-galaxy-tab-s3-book-10-va-book-12-110586.html',
    #     'http://viettimes.vn/mwc-2017-viettel-trinh-dien-hang-loat-san-pham-cong-nghe-thong-tin-110641.html',
    #     'http://viettimes.vn/smartphone-lg-g6-chac-chan-ho-tro-chong-nuoc-109916.html',
    #     'http://viettimes.vn/nga-lo-mo-hinh-may-bay-nem-bom-chien-luoc-the-he-moi-video-109941.html'
    # ]

    # urls = [
    #     'https://cafeland.vn/du-an/khu-phuc-hop-ascott-waterfront-saigon-1271.html',
    #     'https://cafeland.vn/tin-tuc/nguoi-dan-co-bi-ho-khi-dang-mua-chung-cu-hien-nay-65113.html',
    #     'https://cafeland.vn/quy-hoach/quyet-thu-hoi-du-an-kcn-nam-cam-ranh-cua-vinashin-65115.html',
    #     'https://cafeland.vn/tin-tuc/gia-bat-dong-san-trung-quoc-tang-nhanh-nhat-trong-nam-2016-65111.html'
    # ]

    # urls = ['http://viettimes.vn/donald-trump-phai-ra-nhieu-uu-dai-cho-foxconn-neu-muon-san-xuat-iphone-tai-my-112554.html']

    # urls = [
    #     'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/victoria-s-secret-fashion-show-2016-se-dien-ra-tai-paris.html',
    #     'http://tapchithoitrangtre.com.vn/chan-dung/showbiz/quang-dung-ky-niem-20-nam-ca-hat.html',
    #     'http://tapchithoitrangtre.com.vn/video/huong-dan-lam-dep/bien-hoa-3-phong-cach-di-bien-trong-nhay-mat.html',
    #     'http://tapchithoitrangtre.com.vn/video/video-hau-truong/gai-gia-lam-chieu-dinh-trang-chup-hinh.html',
    #     'http://tapchithoitrangtre.com.vn/tin-tuc/tin-cap-nhat/phan-dinh-tung-ra-album-y-niem-5-nam-ngay-cuoi.html',
    #     'http://tapchithoitrangtre.com.vn/tin-tuc/tin-cap-nhat/khi-cac-nghe-si-tranh-luan-chuyen-tinh-thuong-con-cai.html',
    #     'http://tapchithoitrangtre.com.vn/phong-cach/lam-dep/nhung-meo-giup-long-mi-ban-trong-dai-hon.html',
    #     'http://tapchithoitrangtre.com.vn/phong-cach/lam-dep/m-a-c-tiep-tuc-gay-sot-voi-dong-phan-mat-moi.html',
    #     'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/hai-net-doi-lap-trong-bst-moi-cua-lanvin.html',
    #     'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/dries-van-noten-ky-niem-buoi-trinh-dien-lan-thu-100-tai-pfw-thu-dong-2017.html',
    #     'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/ngam-nhung-xu-huong-streetstyle-noi-bat-tai-paris-nam-2017.html',
    #     'http://tapchithoitrangtre.com.vn/song-khoe/suc-khoe/tap-luyen-tai-nha-tai-sao-khong.html'
    # ]

    # urls = [
    #     'https://www.techcombank.com.vn/khach-hang-ca-nhan/chuong-trinh-uu-dai/khuyen-mai-cho-san-pham/kham-pha-the-gioi-am-thuc-cung-the-tin-dung-techcombank-visa',
    #     'https://www.techcombank.com.vn/khach-hang-ca-nhan/chuong-trinh-uu-dai/khuyen-mai-cho-san-pham/sai-canh-binh-an-loc-toi-ngap-tran',
    #     'https://www.techcombank.com.vn/khach-hang-ca-nhan/chuong-trinh-uu-dai/khuyen-mai-cho-san-pham/nghi-ngoi-thoa-thich-tich-luy-dam-bay'
    # ]
    urls = ['http://ione.vnexpress.net/tin-tuc/chiem-tinh/trac-nghiem/tiet-lo-4-pham-chat-tot-dep-nhat-trong-con-nguoi-ban-qua-1-cau-hoi-3592934.html']

    for url in urls:
        result = news_normalizer.normalize(url=url, timeout=15)
        content = result.get_content()
        print(len(content))
        print(json.dumps(content, indent=4, ensure_ascii=False))


def try_checker():
    news_checker = Checker()

    urls = [
        # 'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/victoria-s-secret-fashion-show-2016-se-dien-ra-tai-paris.html',
        # 'http://tapchithoitrangtre.com.vn/chan-dung/showbiz/quang-dung-ky-niem-20-nam-ca-hat.html',
        # 'http://tapchithoitrangtre.com.vn/video/huong-dan-lam-dep/bien-hoa-3-phong-cach-di-bien-trong-nhay-mat.html',
        # 'http://tapchithoitrangtre.com.vn/video/video-hau-truong/gai-gia-lam-chieu-dinh-trang-chup-hinh.html',
        # 'http://tapchithoitrangtre.com.vn/tin-tuc/tin-cap-nhat/phan-dinh-tung-ra-album-y-niem-5-nam-ngay-cuoi.html',
        # 'http://tapchithoitrangtre.com.vn/tin-tuc/tin-cap-nhat/khi-cac-nghe-si-tranh-luan-chuyen-tinh-thuong-con-cai.html',
        # 'http://tapchithoitrangtre.com.vn/phong-cach/lam-dep/nhung-meo-giup-long-mi-ban-trong-dai-hon.html',
        # 'http://tapchithoitrangtre.com.vn/phong-cach/lam-dep/m-a-c-tiep-tuc-gay-sot-voi-dong-phan-mat-moi.html',
        # 'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/hai-net-doi-lap-trong-bst-moi-cua-lanvin.html',
        # 'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/dries-van-noten-ky-niem-buoi-trinh-dien-lan-thu-100-tai-pfw-thu-dong-2017.html',
        # 'http://tapchithoitrangtre.com.vn/phong-cach/thoi-trang/ngam-nhung-xu-huong-streetstyle-noi-bat-tai-paris-nam-2017.html',
        # 'http://tapchithoitrangtre.com.vn/song-khoe/suc-khoe/tap-luyen-tai-nha-tai-sao-khong.html'
    ]

    for url in urls:
        result = news_checker.check(url=url, timeout=15)
        print(result.get_content())


def main():
    # try_crawler()
    try_normalizer()
    # try_checker()
    return


if __name__ == '__main__':
    main()
