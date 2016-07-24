"""
An example of thread deadlock in a readers/writers implementation.
"""
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import random
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class ReadersWriters:

    def __init__(self):
        self.mutex = Lock()
        self.file_lock = Lock()
        self.reader_count = 0

    def write(self, data, loc):
        with self.file_lock:
            with open("dbfile", "w") as dbfile:
                dbfile.seek(loc)
                dbfile.write(data)
        return 'write'

    def read(self, loc, count):
        try:
            with self.mutex:
                self.reader_count += 1
                if self.reader_count == 1:
                    self.file_lock.acquire()
        
            with open("dbfile", "r") as dbfile:
                dbfile.seek(loc)
                result = dbfile.read(count)

            with self.mutex:
                self.reader_count -= 1
                if self.reader_count == 0:
                    self.file_lock.release()
        except Exception as ex:
            log.debug("error: %s", ex)

        return 'read'


READS = ((4, 42), (10, 2), (48, 9), (18, 4), (0, 10), (30, 6), (20, 20), (3, 3))
WRITES = (('foo', 0), ('and what happens now', 14),
          ('take a break and see what happens', 29),
          ('write this and tell me how it goes today', 49))

open("dbfile", "w").close()  # initialize dbfile
rw = ReadersWriters()
pool = ThreadPoolExecutor(max_workers=5)
results = []
while 1:
    for _ in range(1, random.randint(1, 50000)):
        if random.choice((True, True, False)):
            results.append(pool.submit(rw.read, *random.choice(READS)))
        else:
            results.append(pool.submit(rw.write, *random.choice(WRITES)))

    for result in as_completed(results):
        log.info("Finished %s", result.result())
    log.info("** Batch done **")
