# -*- coding: utf-8 -*-

import logging
import threading
import multiprocessing
from reader import DataReader
logging.basicConfig(level=logging.INFO)


class DataProvider:
    def __init__(self):
        logging.info(u'create DataProvider object')
        self.pipe_send, pipe1 = multiprocessing.Pipe()
        self.pipe_recv, pipe2 = multiprocessing.Pipe()
        logging.info(u'create data process')
        self.process = multiprocessing.Process(target=data_process, name=u'data', args=(pipe1, pipe2))
        self.process.start()

    def __del__(self):
        pass

    def read(self):
        pass


class RealDataWorker:
    def __init__(self, pipe_recv, pipe_send):
        self.pipe_recv, self.pipe_send = pipe_recv, pipe_send

        self.queue_data = multiprocessing.Queue()
        self.queue_recv = multiprocessing.Queue()
        self.queue_send = multiprocessing.Queue()

        self.thread_data = threading.Thread(target=self.data_worker)
        self.thread_recv = threading.Thread(target=self.receiver)
        self.thread_send = threading.Thread(target=self.sender)

        self.reader = DataReader()
        self.thread_data.start()
        self.thread_recv.start()
        self.thread_send.start()

        logging.info(u'RealDataWorker - init finish')

    def __del__(self):
        pass

    def receiver(self):
        logging.info(u'start receiver thread')
        while True:
            c = self.pipe_recv.recv()
            if c == 'stop':
                self.queue_recv.put(None)
                self.queue_send.put(None)
                self.queue_data.put(None)
            else:
                self.queue_recv.put(c)

    def sender(self):
        logging.info(u'start sender thread')
        try:
            while True:
                to_send = self.queue_send.get()
                if to_send is None:
                    return
                self.pipe_send.send(to_send)
        except:
            return

    def data_worker(self):
        logging.info(u'start DataReader thread')
        while True:
            obj = self.queue_recv.get()
            if obj is None:
                return
            self.queue_send.put(self.reader.process(obj))

def data_process(pipe_recv, pipe_send):
    logging.info(u'another process, creating RealDataWorker')
    obj = RealDataWorker(pipe_recv, pipe_send)
