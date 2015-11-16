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
        logging.info(u'load db data')
        self.drugs_data = DrugsDataArray(self)
        self.drugs_types = DrugsTypes(self)
        self.drugs_count = DrugsCount(self)
        logging.info(u'DataReader - init finish')

    def process(self, obj):
        pass


class DrugsDataArray:
    def __init__(self, data_reader):
        self.data_reader = data_reader
        self.array = dict()
        self.data_reader.queue_db_tasks.put((u'read', u'SELECT * FROM drugs_data;'))
        for _id, name, cost, _type in self.data_reader.queue_db_results.get():
            self.array[_id] = DrugsData(_id, name, cost, _type)

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value
        self.data_reader.queue_db_tasks.put((u'write',
                                             u'UPDATE drugs_data SET name=%s, cost=%s, type=%s WHERE id=%s' %
                                             (value[1], value[2], value[3], value[0])))

    def __delitem__(self, key):
        del self.array[key]
        self.data_reader.queue_db_tasks.put((u'write', u'DELETE FROM drugs_data WHERE id=%s' % key))


class DrugsData:
    def __init__(self, _id, name, cost, _type):
        self.id, self.name, self.cost, self.type = _id, name, cost, DrugsTypes[_type]


class DrugsTypes:
    def __init__(self, data_reader):
        self.data_reader = data_reader
        self.array = dict()
        self.data_reader.queue_db_tasks.put((u'read', u'SELECT * FROM drugs_types;'))
        for _id, name in self.data_reader.queue_db_results.get():
            self.array[_id] = name

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value
        self.data_reader.queue_db_tasks.put((u'write', u'UPDATE drugs_types SET name=%s WHERE id=%s' % (value, key)))

    def __delitem__(self, key):
        del self.array[key]
        self.data_reader.queue_db_tasks.put((u'write', u'DELETE FROM drugs_types WHERE id=%s' % key))


class DrugsCount:
    def __init__(self, data_reader):
        self.data_reader = data_reader
        self.array = dict()
        self.data_reader.queue_db_tasks.put((u'read', u'SELECT * FROM drugs_count'))
        for _id, available, sold_week in self.data_reader.queue_db_results.get():
            self[_id] = [available, sold_week]

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value
        self.data_reader.queue_db_tasks.put((u'write', u'UPDATE drugs_count SET available=%s, sold_week=%s'
                                                       u'WHERE id=%s' % (value[0], value[1], key)))

    def __delitem__(self, key):
        del self.array[key]
        self.data_reader.queue_db_tasks.put((u'write', u'DELETE FROM drugs_count WHERE id=%s' % key))
