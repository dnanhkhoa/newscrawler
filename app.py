#!/usr/bin/python
# -*- coding: utf8 -*-
import os

os.environ['PAFY_BACKEND'] = 'internal'

import collections
from normalizer import *
from crawler import *
from helpers import *

# Load cấu hình
configs = read_json('configs.txt')

# Dùng để code nhanh
db = configs.get('database')
category_mapping = configs.get('category_mapping')
priority_mapping = configs.get('priority_mapping')
clusters = configs.get('clusters')
ner_path = configs.get('ner_path')
cluster_api = configs.get('cluster_api')

log_file = None

crawler = Crawler()
normalizer = Normalizer()

# Mở kết nối đến CSDL
mysql = MySQL(user=db.get('user'), password=db.get('password'), db=db.get('db'), host=db.get('host'),
              port=db.get('port'), charset=db.get('charset'))


# Lấy danh sách tất cả các URLs có trong DB
def get_urls_from_db():
    try:
        urls = mysql.fetch_all(sql='SELECT `URL` FROM `article`', params=None)
        return [url.get('URL') for url in urls]
    except Exception as e:
        log(e)
    return None


# Thêm dữ liệu vào DB
def post_data_to_db(url, file_path, category, post_date, post_time, status, publish_date, priority):
    params = {
        'URL': url,
        'Path': file_path,
        'Category': category,
        'Date': post_date,
        'Time': post_time,
        'Status': status,
        'PublishDate': publish_date,
        'ID_Attachment': 0,
        'Priority': priority
    }
    mysql.insert('article', params=params)


# Hàm ghi file raw hỗ trợ UTF-8
def write_raw(obj, file_name):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            r = [
                obj.get('SourcePage'),
                obj.get('Title'),
                obj.get('Tag'),
                'ShortIntro',
                obj.get('ShortIntro'),
                'Content',
                obj.get('Plain_Content')
            ]
            f.write(('\r\n'.join(r) + '\r\n').encode('UTF-8'))
        except Exception as e:
            log(e)


# Gửi yêu cầu cluster
def notify_cluster():
    res = requests.get(url=cluster_api)
    if res.status_code == requests.codes.ok:
        write_lines([res.content.decode('UTF-8')], 'response.txt')


def main():
    global log_file
    try:
        # Đường dẫn đến thư mục chứa các clusters
        cluster_path = '%s/%s' % (clusters, str(date.today()).replace('-', ''))

        # Tạo thư mục nếu chưa có
        make_dirs(cluster_path)
        make_dirs(ner_path)

        # Map lưu các URLs theo từng chuyên mục
        categories_urls = collections.defaultdict(lambda: [])

        # Đọc danh sách URLs chuyên mục
        lines = read_lines(configs.get('category_file'))
        for line in lines:
            category_id, url = line.split(' ')
            categories_urls[category_id].append(url)

        # Danh sách các URLs đã crawl
        urls_in_db = get_urls_from_db()
        if urls_in_db is None:
            return None

        # Hotfix for viettimes.vn
        for i, url in enumerate(urls_in_db):
            if 'viettimes.vn' in url:
                urls_in_db[i] = regex.sub(r'-\d+.html', '', url, flags=regex.IGNORECASE)

        # Lặp qua từng chuyên mục
        for category_id in categories_urls:
            # Lấy danh sách các đầu báo thuộc chuyên mục đó
            category_urls = categories_urls.get(category_id)

            category = category_mapping.get(category_id)
            if category is None:
                continue

            with open(path('%s/%s.nerpath' % (ner_path, category)), 'w') as f:
                for category_url in category_urls:
                    priority = priority_mapping.get(category_url)
                    if priority is None:
                        continue

                    try:
                        result = crawler.crawl(url=category_url)
                        if not result.is_ok():
                            continue

                        org_post_urls = result.get_content()
                        if org_post_urls is None or len(org_post_urls) == 0:
                            continue

                        post_urls = []
                        post_urls_in_db = []

                        for url in org_post_urls:
                            if url not in urls_in_db:
                                if 'viettimes.vn' in url:
                                    temp_url = regex.sub(r'-\d+.html', '', url, flags=regex.IGNORECASE)
                                    if temp_url not in urls_in_db:
                                        post_urls.append(url)
                                        post_urls_in_db.append(temp_url)
                                    continue

                                post_urls.append(url)
                                post_urls_in_db.append(url)

                        urls_in_db.extend(post_urls_in_db)

                        # Log danh sách URLS
                        for post_url in post_urls:
                            log_file.write('%s\n' % post_url)

                        for post_url in post_urls:
                            try:
                                result = normalizer.normalize(url=post_url)
                                if not result.is_ok():
                                    post_data_to_db(post_url, '', category, str(date.today()),
                                                    datetime.now().strftime('%H:%M:%S'), 0,
                                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'), priority)
                                    continue

                                content = result.get_content()

                                publish_date = content.get('PublishDate')

                                file_name = '%s/%s/%sK' % (
                                    cluster_path, category, datetime.now().strftime('%H%M%S%f')[:-3])

                                write_json(content, file_name + '.txt')
                                write_raw(content, file_name + '.raw')

                                f.write(os.path.dirname(path()) + file_name[2:] + '.raw.tok\r\n')

                                post_data_to_db(post_url, file_name[2:] + '.txt', category, str(date.today()),
                                                datetime.now().strftime('%H:%M:%S'), 1, publish_date, priority)
                            except Exception as e:
                                debug(post_url)
                                log(e)
                    except Exception as e:
                        debug(category_url)
                        log(e)
    except Exception as e:
        log(e)


if __name__ == '__main__':
    global log_file

    # Ghi lịch sử thực thi
    log_folder = 'log'
    make_dirs(log_folder)

    log_file = open(path(log_folder + '/' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')), 'w')
    log_file.write('Running...\n')

    main()
    notify_cluster()

    log_file.write('Done.\n')
    log_file.close()
