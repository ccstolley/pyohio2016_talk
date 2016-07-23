from threading import Thread
import queue

class WorkerPool(object):

    def __init__(self):
        self.resultq = queue.Queue()
        self.workq = queue.Queue()

    def execute(self, jobs):
        for job in jobs:
            self.workq.put_nowait(job)
        threads = [Thread(target=self._worker) for i in range(10)]
        for t in threads:
            t.isDaemon = True
            t.start()
        for t in threads:
            t.join()
            if t.isAlive():
                break

        results = {}
        while not self.resultq.empty():
            results.update(self.resultq.get())
        return results

    def _worker(self):
        while not self.workq.empty():
            job = self.workq.get()
            result = fetch_data(job)
            if result is not None:
                self.resultq.put(result)


def fetch_data(job):
    return {"foo" + str(job): id(job)}


wp = WorkerPool()
print(wp.execute([str(i) for i in range(4000)]))
