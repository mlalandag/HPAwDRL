import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

class WorkerThread(threading.Thread):
    
    def __init__(self, task, **kwargs):
        super(WorkerThread, self).__init__(**kwargs)
        self.task   = task

    def run(self):
        logging.debug("starting %s" % (self.task.file))
        self.task.run()
        logging.debug("done %s" % (self.task.file))
        

class Worker():
    
    def __init__(self):
        self.thr    = None

    def run_task(self, task):    
        if self.thr != None and self.thr.is_alive():
            self.thr.join()
        self.thr  = WorkerThread(task)
        self.thr.start()
        logging.debug("%s Launched" % (task.file))
            
    def is_running(self):
        if self.thr == None:
            return False
        else:
            return self.thr.is_alive()


class WorkerPool():
    
    def __init__(self, max_workers, initial_workers):
        self.pool = []
        self.number_of_workers = 0
        self.max_workers = max_workers
        self.avg_time = 0
        for i in range(0,initial_workers):
            wrk = Worker()
            self.add_worker(wrk)
        
    def add_worker(self, worker):
        if self.number_of_workers < self.max_workers:
            self.pool.append(worker)
            self.number_of_workers += 1
        
    def remove_worker(self):
        deleted = False
        while True:
            for wrk in self.pool:
                if not wrk.is_running():
                    self.pool.remove(wrk)
                    self.number_of_workers -= 1
                    deleted = True
                    break
            if (deleted or self.number_of_workers == 0):
                break
        
    def get_num_workers(self):
        return self.number_of_workers

    def get_num_workers_running(self):
        count = 0
        for wrk in self.pool:
            if wrk.is_running():
                count += 1
        return count