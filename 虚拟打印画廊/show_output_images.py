import tkinter as tk
import json
import os
from PIL import Image, ImageTk
import tkinter.messagebox as msgbox


def get_label_dimensions(label):
    """
    获取给定tk.Label的坐标信息及尺寸信息
    """
    label.update_idletasks()
    x, y, width, height = label.bbox()
    return x, y, width, height


def update_vertical_offset(vertical_offset, label):
    """
    根据给定的标签更新垂直偏移量
    """
    _, y, _, height = get_label_dimensions(label)
    return max(vertical_offset, y + height)


def create_card(frame, task_info):
    """
    创建一个卡片，包含任务信息和图片（如果有），并返回卡片的框架
    """
    card_frame = tk.Frame(frame, bd=2, relief=tk.SOLID)
    card_frame.pack(side=tk.LEFT, padx=5, pady=5)  # 初始设置为横向排列，后续根据布局情况调整

    task_id = task_info["task_id"]
    file_path = task_info["file_path"]
    title = task_info["title"]
    author = task_info["author"]
    description = task_info["description"]
    timestamp = task_info["timestamp"]

    task_info_text = f"任务ID: {task_id}\n" \
                     f"文件路径: {file_path}\n" \
                     f"标题: {title}\n" \
                     f"作者: {author}\n" \
                     f"描述: {description}\n" \
                     f"时间戳: {timestamp}\n"
    info_label = tk.Label(card_frame, text=task_info_text, justify=tk.LEFT)
    info_label.pack(pady=(5, 0))

    # 判断文件路径是否为图片格式，如果是则加载展示图片
    file_extension = os.path.splitext(file_path)[1]
    if file_extension in ['.png', '.jpg', '.gif']:
        try:
            image = Image.open(file_path)

            # 动态计算图片缩放比例（示例，可根据实际调整）
            max_image_width = 150
            scale_factor = max_image_width / image.size[0]
            new_width = int(image.size[0] * scale_factor)
            new_height = int(image.size[1] * scale_factor)

            # 调整图片大小并使用Image.Resampling.LANCZOS实现抗锯齿效果
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            photo_image = ImageTk.PhotoImage(image)

            photo_label = tk.Label(card_frame, image=photo_image, width=new_width, height=new_height)
            photo_label.image = photo_image
            photo_label.pack(pady=(5, 0))

        except Exception as e:
            msgbox.showerror("图片加载错误", f"加载图片 {file_path} 时出错: {e}")

    return card_frame


def create_show_images_interface(output_buffer):
    root = tk.Toplevel()
    root.title("加载输出井图片展示界面")

    # 创建一个主框架，用于放置滚动条、内容容器以及下拉框等组件
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建一个滚动条
    scrollbar = tk.Scrollbar(main_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建一个Canvas作为内容容器，用于放置所有的卡片内容
    content_canvas = tk.Canvas(main_frame, bg='white')
    content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 将滚动条与内容Canvas进行关联
    scrollbar.config(command=content_canvas.yview)
    content_canvas.config(yscrollcommand=scrollbar.set)

    # 用于记录当前行的卡片宽度总和，用于判断是否换行
    current_row_width = 0
    max_row_width = root.winfo_screenwidth() - 50  # 大致根据屏幕宽度设置一行可容纳的最大宽度，可调整

    # 创建一个下拉框（示例，可根据实际需求添加具体功能选项）
    options = ["选项1", "选项2", "选项3"]
    selected_option = tk.StringVar()
    selected_option.set(options[0])
    dropdown = tk.OptionMenu(content_canvas, selected_option, *options)
    dropdown.pack(side=tk.RIGHT, padx=10, pady=10)

    # 用于记录内容在Canvas中的垂直偏移量，初始化为0
    vertical_offset = 0

    for task_info in output_buffer:
        card_frame = create_card(content_canvas, task_info)

        # 获取卡片框架的宽度
        card_frame.update_idletasks()
        _, _, card_width, _ = get_label_dimensions(card_frame)

        if current_row_width + card_width > max_row_width:
            # 如果当前行宽度超过最大行宽，换行排列
            card_frame.pack_forget()
            card_frame.pack(side=tk.LEFT, padx=5, pady=5)
            current_row_width = card_width
            vertical_offset += 10  # 适当增加垂直偏移量，避免卡片太紧凑
        else:
            current_row_width += card_width

        # 更新垂直偏移量，基于卡片框架的高度
        vertical_offset = update_vertical_offset(vertical_offset, card_frame)

    # 在所有内容添加完毕后，设置Canvas的滚动区域
    content_canvas.update_idletasks()
    content_canvas.config(scrollregion=(0, 0, 0, vertical_offset))