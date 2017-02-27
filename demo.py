#!/usr/bin/python
# -*- coding: utf8 -*-

import os

os.environ['PAFY_BACKEND'] = 'internal'

from crawler import *
from normalizer import *
from helpers import *
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
    #     'http://nongnghiep.vn/giai-tri-27-15.html',
    #     'http://nongnghiep.vn/giao-duc-28-15.html',
    #     'http://nongnghiep.vn/kinh-te-3-15.html',
    #     'http://nongnghiep.vn/phap-luat-15-15.html',
    #     'http://nongnghiep.vn/the-gioi-8-15.html',
    #     'http://nongnghiep.vn/the-thao-29-15.html',
    #     'http://nongnghiep.vn/van-hoa-26-15.html'
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

    urls = [
        'http://ngoisao.net/tin-tuc/thoi-cuoc/24h',
        'http://ngoisao.net/tin-tuc/thoi-cuoc/thuong-truong',
        'http://ngoisao.net/tin-tuc/hau-truong/showbiz-viet',
        'http://ngoisao.net/tin-tuc/hau-truong/chau-a',
        'http://ngoisao.net/tin-tuc/hau-truong/hollywood',
        'http://ngoisao.net/tin-tuc/thu-gian/dan-choi',
        'http://ngoisao.net/tin-tuc/phong-cach/lam-dep/xu-huong',
        'http://ngoisao.net/tin-tuc/phong-cach/lam-dep/sao-dep',
        'http://ngoisao.net/tin-tuc/phong-cach/lam-dep/bi-quyet',
        'http://ngoisao.net/tin-tuc/phong-cach/thoi-trang/hot-trend',
        'http://ngoisao.net/tin-tuc/phong-cach/thoi-trang/sao-style',
        'http://ngoisao.net/tin-tuc/phong-cach/thoi-trang/tu-van',
        'http://ngoisao.net/tin-tuc/thu-gian/an-choi/an',
        'http://ngoisao.net/tin-tuc/thu-gian/an-choi/choi'

    ]

    from_date = '2017-02-20'  # Để None nếu muốn lấy thời gian min hiện tại (%Y-%m-%d 00:00:00)
    to_date = '2017-02-20'  # Để None nếu muốn lấy thời gian max hiện tại (%Y-%m-%d 23:59:59)
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

    # urls = [
    #     'http://nongnghiep.vn/video-trung-quoc-xay-cau-phao-dai-hon-1000-m-trong-27-phut-post183533.html',
    #     'http://nongnghiep.vn/video-nguoi-dan-ong-bi-dan-ho-vo-den-chet-trong-vuon-thu-trung-quoc-post186004.html',
    #     'http://nongnghiep.vn/video-nu-cau-tac-bi-deo-cho-chet-vao-co-post177680.html',
    #     'http://nongnghiep.vn/video-kim-jong-nam-bi-sat-hai-nhu-the-nao-post187146.html',
    #     'http://nongnghiep.vn/tung-doan-xe-noi-dai-truoc-cong-lam-thao-post186584.html',
    #     'http://nongnghiep.vn/nu-sinh-tphcm-se-mac-ao-dai-it-nhat-2-buoi-tuan-post186679.html',
    #     'http://nongnghiep.vn/tao-dieu-kien-thuan-loi-cung-ung-dich-vu-giao-duc-dao-tao-post186386.html'
    # ]

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
    #     'http://ngoisao.net/tin-tuc/hau-truong/showbiz-viet/phat-ngon-khong-the-bo-qua-cua-sao-viet-trong-tuan-31-3544255.html',
    #     'http://ngoisao.net/tin-tuc/hau-truong/hollywood/channing-tatum-be-bong-vo-yeu-tren-bai-bien-3544034.html',
    #     'http://ngoisao.net/tin-tuc/thoi-cuoc/24h/nguoi-phu-nu-viet-bi-chong-sat-hai-o-my-3544198.html',
    #     'http://ngoisao.net/tin-tuc/thoi-cuoc/24h/nguoi-phu-nu-280-kg-cau-xin-duoc-cuu-3542651.html',
    #     'http://ngoisao.net/tin-tuc/thoi-cuoc/24h/ca-co-gai-toi-cuu-lan-ke-dam-dao-chua-ai-den-hoi-tham-3542821.html'
    # ]

    urls = [
        'http://giaoducthoidai.vn/thoi-su/nhom-nguoi-nuoc-ngoai-dung-the-atm-gia-rut-trom-tien-2963790-l.html'
    ]

    for url in urls:
        result = news_normalizer.normalize(url=url, timeout=15)
        print(json.dumps(result.get_content(), indent=4, ensure_ascii=False))


def main():
    # try_crawler()
    try_normalizer()
    return


if __name__ == '__main__':
    main()
