import tkinter as tk
import json
import os

import 虚拟打印画廊
from load_tasks_to_queue import print_queue, load_tasks_to_queue
from print_gallery import input_spool_dir
from show_output_images import create_show_images_interface

# 创建主窗口
root = tk.Tk()
root.title("任务队列展示界面")

# 用于显示任务队列信息的文本框
queue_text = tk.Text(root)
queue_text.pack()

# 加载按钮
load_button = tk.Button(root, text="加载并展示任务队列", command=lambda: display_queue())
load_button.pack()


def display_queue():
    global print_queue
    # 先清空之前的显示内容
    queue_text.delete('1.0', tk.END)

    # 重新从输入井加载任务到打印队列（假设采用先来先服务顺序）
    load_tasks_to_queue()

    # 遍历打印队列并展示任务信息
    for task in print_queue:
        task_info = f"任务ID: {task['task_id']}\n" \
                    f"文件路径: {task['file_path']}\n" \
                    f"标题: {task['title']}\n" \
                    f"作者: {task['author']}\n" \
                    f"描述: {task['description']}\n" \
                    f"状态: {task['status']}\n" \
                    f"时间戳: {task['timestamp']}\n\n"
        queue_text.insert(tk.END, task_info)
    return create_show_images_interface(print_queue)


if __name__ == "__main__":
    root.mainloop()