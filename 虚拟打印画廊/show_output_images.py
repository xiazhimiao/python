import tkinter as tk
import json
import os
from PIL import Image, ImageTk


def create_show_images_interface(output_buffer):
    root = tk.Toplevel()
    root.title("输出缓冲区图片展示界面")

    # 创建一个主框架，用于放置滚动条和内容容器（这里改为Canvas）
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建一个滚动条
    scrollbar = tk.Scrollbar(main_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建一个Canvas作为内容容器，用于放置所有的任务信息和图片等内容
    content_canvas = tk.Canvas(main_frame, bg='white')
    content_canvas.pack(fill=tk.BOTH, expand=True)

    # 将滚动条与内容Canvas进行关联
    scrollbar.config(command=content_canvas.yview)
    content_canvas.config(yscrollcommand=scrollbar.set)

    # 用于记录内容在Canvas中的垂直偏移量，初始化为0
    vertical_offset = 0

    for task_info in output_buffer:
        frame = tk.Frame(content_canvas)
        frame.pack()

        task_id = task_info["task_id"]
        file_path = task_info["file_path"]
        title = task_info["title"]
        author = task_info["author"]
        description = task_info["description"]
        status = task_info["status"]
        timestamp = task_info["timestamp"]

        task_info_text = f"任务ID: {task_id}\n" \
                         f"文件路径: {file_path}\n" \
                         f"标题: {title}\n" \
                         f"作者: {author}\n" \
                         f"描述: {description}\n" \
                         f"状态: {status}\n" \
                         f"时间戳: {timestamp}\n"
        info_label = tk.Label(frame, text=task_info_text)
        info_label.pack()

        # 获取当前任务信息标签在Canvas中的坐标信息
        info_label.update_idletasks()
        info_label_x, info_label_y, info_label_width, info_label_height = info_label.bbox()

        # 更新垂直偏移量，加上任务信息标签的高度
        vertical_offset = max(vertical_offset, info_label_y + info_label_height)

        # 判断文件路径是否为图片格式，如果是则加载展示图片
        file_extension = os.path.splitext(file_path)[1]
        if file_extension in ['.png', '.jpg', '.gif']:
            try:
                print(file_path)
                image = Image.open(file_path)

                # 获取原始图片的宽度和高度
                original_width, original_height = image.size

                # 计算缩小后的宽度和高度（这里假设你可能还想对图片进行缩小处理，可根据实际需求调整）
                new_width = int(original_width * 0.1)
                new_height = int(original_height * 0.1)

                # 调整图片大小并使用Image.Resampling.LANCZOS实现抗锯齿效果
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                photo_image = ImageTk.PhotoImage(image)

                # 定义图片框（即用于展示图片的tk.Label）的大小
                photo_label = tk.Label(frame, image=photo_image, width=new_width, height=new_height)
                photo_label.image = photo_image
                photo_label.pack()

                # 获取当前图片标签在Canvas中的坐标信息
                photo_label.update_idletasks()
                photo_label_x, photo_label_y, photo_label_width, photo_label_height = photo_label.bbox()

                # 更新垂直偏移量，加上图片标签的高度
                vertical_offset = max(vertical_offset, photo_label_y + photo_label_height)

            except Exception as e:
                print(f"加载图片 {file_path} 时出错: {e}")

    # 在所有内容添加完毕后，设置Canvas的滚动区域
    content_canvas.update_idletasks()
    content_canvas.config(scrollregion=(0, 0, 0, vertical_offset))

    root.mainloop()