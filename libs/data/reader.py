# -*- coding: utf-8 -*-

import logging
import threading
import multiprocessing
import db
logging.basicConfig(level=logging.INFO)


class DataReader:
    def __init__(self):
        logging.info(u'create DataReader object')
        self.queue_db_tasks = multiprocessing.Queue()
        self.queue_db_results = multiprocessing.Queue()
        logging.info(u'create db thread')
        self.thread_db = threading.Thread(target=db.db_thread, args=(self.queue_db_tasks, self.queue_db_results))
        self.thread_db.start()
        logging.info(u'DataReader - init finish')

    def process(self, obj):
        pass
