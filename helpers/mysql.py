#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
import pymysql

from helpers import *


class MySQL(object):
    def __init__(self, user, password, db, host='localhost', port=3306, charset='utf8mb4'):
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
                if func is not None:
                    return func(connection, cursor)
        except Exception as e:
            log(e)
        finally:
            if connection is not None:
                connection.close()

    def fetch_one(self, sql, params):
        pass

    def fetch_all(self, sql, params):
        pass

    def get_all(self, table, fields='*'):
        def do(connection, cursor):
            sql = 'SELECT %s FROM %s'
            cursor.execute(sql, (fields, table))
            return cursor.fetchall()

        return self.query(do)
