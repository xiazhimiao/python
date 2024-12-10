import tkinter as tk
import json
import os

import 虚拟打印画廊
from load_tasks_to_queue import print_queue, load_tasks_to_queue
from task_submission import input_spool_dir
from show_output_images import create_show_images_interface
from user_processing_procedure import output_spool_dir, user_processing_procedure

# 创建主窗口
root = tk.Toplevel()
root.title("任务队列展示界面")

# 用于显示任务队列信息的文本框
queue_text = tk.Text(root)
queue_text.pack()

# 加载按钮
load_button = tk.Button(root, text="加载并展示任务队列", command=lambda: display_queue())
load_button.pack()


def display_queue():
    global print_queue, user_processing_procedure
    # 先清空之前的显示内容
    queue_text.delete('1.0', tk.END)

    # 重新从输入井加载任务到打印队列（假设采用先来先服务顺序）
    print_queue = load_tasks_to_queue(input_spool_dir)

    if not print_queue:
        queue_text.insert(tk.END, '任务队列暂时没有内容')
    else:
        # 这里模拟用户进程进行任务处理：
        # 把从输入井加载来的内容，发送给用户进程处理
        # 用户进程处理后存储到输出井
        # print(type(print_queue))
        user = user_processing_procedure(print_queue)
        user.process_tasks()

        output_buffer = load_tasks_to_queue(output_spool_dir)

        # 遍历打印队列并展示任务信息
        for task in output_buffer:
            task_info = f"任务ID: {task['task_id']}\n" \
                        f"文件路径: {task['file_path']}\n" \
                        f"标题: {task['title']}\n" \
                        f"作者: {task['author']}\n" \
                        f"描述: {task['description']}\n" \
                        f"时间戳: {task['timestamp']}\n\n"
            queue_text.insert(tk.END, task_info)
        return create_show_images_interface(output_buffer)


if __name__ == "__main__":
    root.mainloop()
