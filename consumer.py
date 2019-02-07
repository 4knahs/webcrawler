# For Process-based threading
import multiprocessing
from logger import warn, info, debug, error


class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        """Consumer task processing function. Retrieves a task, i.e., an URL, from 
        a tasks queue and finds new URLs within its content. These URLs are then 
        written to a result queue that gets validated by the producer for URL
        freshness.
        """
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                debug('{}: Exiting'.format(proc_name))
                self.task_queue.task_done()
                break
            debug('{}: {}'.format(proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return