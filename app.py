#!/usr/bin/python
# -*- coding: utf8 -*-
import os

os.environ['PAFY_BACKEND'] = 'internal'

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

crawler = Crawler()
normalizer = Normalizer()

# Mở kết nối đến CSDL
mysql = MySQL(user=db.get('user'), password=db.get('password'), db=db.get('db'), host=db.get('host'),
              port=db.get('port'), charset=db.get('charset'))


def get_id_from_db(category):
    count = mysql.fetch_one(sql='SELECT COUNT(ID) AS `CNT` FROM `article` WHERE Date = %s and Category = %s',
                            params=(str(date.today()), category))
    return None if count is None else count.get('CNT')


def get_urls_from_db():
    try:
        urls = mysql.fetch_all(sql='SELECT `URL` FROM `article`', params=None)
        return [url.get('URL') for url in urls]
    except Exception as e:
        log(e)
    return None


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
                obj['SourcePage'],
                obj['Title'],
                obj['Tag'],
                'ShortIntro',
                obj["ShortIntro"],
                'Content',
                obj["Plain_Content"]
            ]
            f.write(('\n'.join(r) + '\n').encode('UTF-8'))
        except Exception as e:
            log(e)


def main():
    try:
        cluster_path = '%s/%s' % (clusters, str(date.today()).replace('-', ''))
        make_dirs(cluster_path)
        make_dirs(ner_path)

        lines = read_lines(configs.get('category_file'))
        urls_in_db = get_urls_from_db()
        if urls_in_db is None:
            return None

        for line in lines:
            _id, url = line.split(' ')
            category = category_mapping.get(_id)
            priority = priority_mapping.get(url)
            if _id is None or url is None or category is None or priority is None:
                continue

            try:
                post_urls = crawler.crawl(url=url)
                if post_urls is None or len(post_urls) == 0:
                    continue

                post_urls = list(set(post_urls) - set(urls_in_db))

                max_id = get_id_from_db(category) + 1

                with open(path('%s/%s.nerpath' % (ner_path, category)), 'w') as f:
                    for post_url in post_urls:
                        try:
                            result = normalizer.normalize(url=post_url)

                            source_url = result['Url']
                            publish_date = result['PublishDate']

                            file_name = '%s/%s/%d' % (cluster_path, category, max_id)

                            write_json(result, file_name + '.txt')
                            write_raw(result, file_name + '.raw')

                            post_data_to_db(source_url, file_name[2:] + '.txt', category, str(date.today()),
                                            datetime.now().strftime('%H:%M:%S'), 0, publish_date, priority)

                            f.write(os.path.dirname(os.path.dirname(path())) + file_name[2:] + '.raw.tok\n')

                            max_id += 1
                        except Exception as e:
                            log(e)
                            continue

            except Exception as e:
                log(e)
                continue
    except Exception as e:
        log(e)


if __name__ == '__main__':
    print('Running')
    main()
    print('Done')
