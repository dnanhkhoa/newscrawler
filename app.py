#!/usr/bin/python
# -*- coding: utf8 -*-
import os

os.environ['PAFY_BACKEND'] = 'internal'

from normalizer import *
from crawler import *
from helpers import *

configs = read_json('configs.txt')
db = configs.get('database')
category_mapping = configs.get('category_mapping')
priority_mapping = configs.get('priority_mapping')
clusters = configs.get('clusters')

mysql = MySQL(user=db.get('user'), password=db.get('password'), db=db.get('db'), host=db.get('host'),
              port=db.get('port'))


def get_id_from_db(category):
    def do(connection, cursor):
        sql = 'SELECT COUNT(ID) AS `ID` FROM `article` WHERE Date = %s and Category = %s'
        cursor.execute(sql, (str(date.today()), category))
        return cursor.fetchone()

    id = mysql.query(do)
    return None if id is None else id.get('ID')


def get_urls_from_db():
    def do(connection, cursor):
        sql = 'SELECT URL FROM `article`'
        cursor.execute(sql)
        return cursor.fetchall()

    urls = mysql.query(do)
    return [url.get('URL') for url in urls]


def post_data_to_db(url, file_path, category, post_date, post_time, status, publish_date, priority):
    def do(connection, cursor):
        sql = 'INSERT INTO `article` (`URL`, `Path`, `Category`, `Date`, `Time`, `Status`, `PublishDate`, `ID_Attachment`, `Priority`)' \
              ' VALUES (%s, %s, %s, %s, %s, %s, %s, 0, %s)'
        cursor.execute(sql, (url, file_path, category, post_date, post_time, status, publish_date, priority))
        connection.commit()

    mysql.query(do)


def main():
    crawler = Crawler()
    normalizer = Normalizer()

    lines = read_lines(configs.get('category_file'))
    urls_in_db = get_urls_from_db()

    for line in lines:
        id, url = line.split(' ')
        category = category_mapping.get(id)
        priority = priority_mapping.get(url)

        if id is None or url is None or category is None or priority is None:
            continue

        try:

            post_urls = crawler.crawl(url=url)
            post_urls = list(set(post_urls) - set(urls_in_db))

            with open('%s/%s/%s/paths.txt' % (clusters, str(date.today()).replace('-', ''), category), 'w') as f:

                max_id = get_id_from_db(category)
                for post_url in post_urls:
                    result = normalizer.normalize(url=post_url)
                    file_name = '%s/%s/%s/%d' % (clusters, str(date.today()).replace('-', ''), category, max_id)
                    print(file_name)
                    write_json(result, file_name + '.txt')

                    # UNSET 3 VARS
                    del result['thumbnail']
                    del result['sourceUrl']
                    write_json(result, file_name + '.raw')

                    post_data_to_db(url, file_name[2:] + '.txt', category, str(date.today()), datetime.now().strftime('%H:%M:%S'), 0, result['publishDate'], priority)

                    f.write(file_name[2:] + '.txt\r\n')

                    max_id += 1

        except Exception  as e:
            log(e)

if __name__ == '__main__':
    main()
