# -*- coding: utf-8 -*-

import logging
import os
from pysqlcipher import dbapi2 as sqlite
logging.basicConfig(level=logging.INFO)


class DbWorker:
    def __init__(self, tasks, results):
        logging.info(u'create DbWorker object')
        self.tasks, self.results = tasks, results
        self.db_name = u'data.sql'
        self.password = 'test'  # TODO: fix with settings reader
        if not os.path.exists(self.db_name):
            logging.info(u'create empty db')
            conn = sqlite.connect(self.db_name)
            with conn:
                cursor = conn.cursor()
                self.init_encryption(cursor)
                cursor.executescript(u'''
                    CREATE TABLE drugs_data     (id INTEGER PRIMARY KEY, name TEXT, cost NUMERIC, type NUMERIC);
                    CREATE TABLE drugs_types    (id INTEGER PRIMARY KEY, name TEXT);
                    CREATE TABLE drugs_count    (id INTEGER PRIMARY KEY, available NUMERIC, sold_week NUMERIC);
                ''')
                conn.commit()
                cursor.close()
        logging.info(u'DbWorker - init finish')

    def loop(self):
        logging.info(u'DbWorker loop')
        conn = sqlite.connect(self.db_name)
        with conn:
            cursor = conn.cursor()
            self.init_encryption(cursor)
            while True:
                task = self.tasks.get()
                if task is None:
                    return
                task_type, sql = task
                if task_type == u'write':
                    cursor.executescript(sql)
                    conn.commit()
                elif task_type == u'read':
                    cursor.execute(sql)
                    conn.commit()
                    self.results.put(cursor.fetchall())

    def init_encryption(self, cursor):
        cursor.execute("PRAGMA key='%s'" % self.password)


def db_thread(tasks, results):
    obj = DbWorker(tasks, results)
    obj.loop()
