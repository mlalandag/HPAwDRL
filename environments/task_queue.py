import collections
import time
import random
import datetime

class Task():
    
    def __init__(self, file):
        self.file = file
        self.duration = 0
        self.creation_date = datetime.datetime.now()
    
    def run(self):
        self.duration = random.random()*100
        time.sleep(self.duration)


class TaskQueue():
    
    def __init__(self):
        self.number_of_tasks = 0
        self.tasks_count = 0        
        self.queue           = collections.deque([]) 
        self.cum_task_duration = 0.0
        self.avg_task_duration = 0.0
        self.cum_time_in_queue = 0.0
        self.avg_time_in_queue = 0.0
        
    def add_task(self, task):
        self.number_of_tasks += 1
        self.tasks_count += 1     
        self.cum_task_duration += task.duration 
        self.avg_task_duration = self.cum_task_duration / self.tasks_count
        self.queue.append(task)
        
    def take_task(self):
        if len(self.queue) > 0:
            task = self.queue.popleft()
            time_in_queue = (datetime.datetime.now() - task.creation_date).total_seconds()
            self.cum_time_in_queue += time_in_queue
            self.avg_time_in_queue = self.cum_time_in_queue / self.tasks_count
            self.number_of_tasks -= 1            
            return task
        
    def get_num_tasks(self):
        return self.number_of_tasks