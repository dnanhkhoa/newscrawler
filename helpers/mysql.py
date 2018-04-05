#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
import pymysql

from helpers import *


class MySQL(object):
    def __init__(self, user, password, db, host='localhost', port=3306, charset='utf8'):
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.charset = charset

    def query(self, func=None):
        connection = None
        try:
            connection = pymysql.connect(host=self.host,
                                         port=self.port,
                                         user=self.user,
                                         password=self.password,
                                         db=self.db,
                                         charset=self.charset,
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                if func:
                    return func(connection, cursor)
        except Exception as e:
            log(e)
        finally:
            if connection:
                connection.close()

    def fetch_one(self, sql, params=None):
        def do(_, cursor):
            cursor.execute(sql, params)
            return cursor.fetchone()

        return self.query(do)

    def fetch_all(self, sql, params=None):
        def do(_, cursor):
            cursor.execute(sql, params)
            return cursor.fetchall()

        return self.query(do)

    def insert(self, table, params):
        def do(connection, cursor):
            sql = 'INSERT INTO `%s` (`%s`) VALUES (%s)' % (
                table, '`, `'.join(params.keys()), ', '.join(['%s'] * len(params)))
            cursor.execute(sql, tuple(params.values()))
            connection.commit()

        self.query(do)
