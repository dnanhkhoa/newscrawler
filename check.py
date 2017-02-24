#!/usr/bin/python
# -*- coding: utf8 -*-
import os

os.environ['PAFY_BACKEND'] = 'internal'

from checker import *
from helpers import *

# Load cấu hình
configs = read_json('configs.txt')

# Dùng để code nhanh
db = configs.get('database')

# Mở kết nối đến CSDL
mysql = MySQL(user=db.get('user'), password=db.get('password'), db=db.get('db'), host=db.get('host'),
              port=db.get('port'), charset=db.get('charset'))

checker = Checker()


# Lấy danh sách tất cả các URLs có trong DB
def get_urls_from_db(params=(14, 16)):
    try:
        urls = mysql.fetch_all(
            sql='SELECT `ID`, `URL` FROM `article` WHERE `Status` > 0 '
                'AND (CURDATE() - `Date`) >= %s AND (CURDATE() - `Date`) <= %s',
            params=params)
        return [(url.get('ID'), url.get('URL')) for url in urls]
    except Exception as e:
        log(e)
    return None


def update_status(id):
    def do(connection, cursor):
        sql = 'UPDATE `article` SET `Status`=0 WHERE `ID` = %s'
        cursor.execute(sql, id)
        connection.commit()

    mysql.query(do)


def main():
    try:
        log_folder = 'check_log'
        make_dirs(log_folder)
        with open(path(log_folder + '/' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')), 'w') as f:
            urls = get_urls_from_db((14, 16))
            for id, url in urls:
                result = checker.check(url=url)
                if result.is_ok():
                    is_live = result.get_content()
                    if not is_live:
                        update_status(id)
                        f.write('Die: %s\r\n' % url)
                else:
                    f.write('Error: %s' % url)
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
