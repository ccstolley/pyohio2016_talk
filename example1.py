"""
An example of a poller that is not robust in the face of a slow or
unreliable server.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

class Poller:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=5)

    def poll(self, jobs):
        return {job: self.pool.submit(self.fetch, job) for job in jobs}

    @staticmethod
    def fetch(job):
        url = 'http://localhost:9999/{}'.format(job)
        starttime = time.time()
        result = requests.get(url).json()
        log.info("Obtained result for %s in %.2f secs",
                 url, time.time() - starttime)
        return result


poller = Poller()
results = poller.poll(str(i) for i in range(40000))
for future in as_completed(results.values()):
    print(future.result())
    # and send the results to a database, message pipeline, etc
