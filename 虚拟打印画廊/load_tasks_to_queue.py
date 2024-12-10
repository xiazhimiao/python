import os
import json
from task_submission import input_spool_dir

output_spool_dir = os.path.join(os.getcwd(), 'output_spool')
input_spool_dir = os.path.join(os.getcwd(), 'input_spool')
# 定义打印队列
print_queue = []


def load_tasks_to_queue(spool):
    global print_queue

    print_queue.clear()  # 先清空打印队列

    task_files = os.listdir(spool)
    for task_file in task_files:
        task_file_path = os.path.join(spool, task_file)
        with open(task_file_path, 'r') as f:
            task_info = json.load(f)
        print_queue.append(task_info)

    return print_queue


# 顺序优先（先来先服务）调度算法实现
def prioritize_queue_fcfs():
    global print_queue
    # 这里已经是按照任务从输入井读取到打印队列的顺序排列，
    # 所以其实不需要额外的排序操作，可直接返回打印队列
    return print_queue
