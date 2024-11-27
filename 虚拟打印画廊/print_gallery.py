import tkinter as tk
from tkinter import filedialog
import os
import json
import time

# 全局变量，用于记录输入井的根目录路径（这里假设在项目根目录下创建一个名为 'input_spool' 的文件夹作为输入井）
input_spool_dir = os.path.join(os.getcwd(), 'input_spool')


# 任务类
class PrintTask:
    def __init__(self, task_id, file_path, title, author, description):
        self.task_id = task_id
        self.file_path = file_path
        self.title = title
        self.author = author
        self.description = description
        self.status = "等待"


# 用户提交模块
def submit_artwork():
    global input_spool_dir
    file_path = filedialog.askopenfilename()
    if file_path:
        title = title_entry.get()
        author = author_entry.get()
        description = description_entry.get()

        # 检查文本框是否为空，如果为空则不允许提交并给出提示
        if not title or not author or not description:
            status_label.config(text="请填写完整作品标题、作者和描述信息后再提交！")
            return

        task_id = len(os.listdir(input_spool_dir)) if os.path.exists(input_spool_dir) else 0
        timestamp = time.time()

        # 创建任务字典
        task = {
            "task_id": task_id,
            "file_path": file_path,
            "title": title,
            "author": author,
            "description": description,
            "status": "等待",
            "timestamp": timestamp
        }

        # 将任务信息保存为JSON文件到输入井目录
        task_file_path = os.path.join(input_spool_dir, f'task_{task_id}.json')
        with open(task_file_path, 'w') as f:
            json.dump(task, f)

        # 提交成功后给出提示并清空文本框
        status_label.config(text=f"作品已提交，任务ID：{task['task_id']}")
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)


# 创建主窗口
root = tk.Tk()
root.title("虚拟打印画廊提交界面")

# 作品标题标签和输入框
title_label = tk.Label(root, text="作品标题：")
title_label.pack()
title_entry = tk.Entry(root)
title_entry.pack()

# 作者标签和输入框
author_label = tk.Label(root, text="作者：")
author_label.pack()
author_entry = tk.Entry(root)
author_entry.pack()

# 描述标签和输入框
description_label = tk.Label(root, text="描述：")
description_label.pack()
description_entry = tk.Entry(root)
description_entry.pack()

# 提交按钮
submit_button = tk.Button(root, text="提交作品", command=submit_artwork)
submit_button.pack()

# 状态标签
status_label = tk.Label(root, text="")
status_label.pack()

# 如果输入井目录不存在，创建它
if not os.path.exists(input_spool_dir):
    os.makedirs(input_spool_dir)

# root.mainloop()