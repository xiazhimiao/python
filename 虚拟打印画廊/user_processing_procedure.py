import os
import json  # 导入json模块，用于处理JSON数据

# 全局变量，用于记录输入井和输出井的根目录路径（这里假设在项目根目录下创建相应文件夹作为输入井和输出井）
output_spool_dir = os.path.join(os.getcwd(), 'output_spool')


class user_processing_procedure:
    def __init__(self, print_queue):
        self.print_queue = print_queue

    def process_tasks(self):
        """
        处理任务队列的方法，将任务信息进行修改并保存为JSON文件到输出井目录
        """
        # 如果输出井目录不存在，创建它
        if not os.path.exists(output_spool_dir):
            os.makedirs(output_spool_dir)

        self.clear_output_spool()

        for task_info in self.print_queue:
            task_info["title"] = task_info["title"] + "| 假设用户进程处理"
            task_id = len(os.listdir(output_spool_dir)) if os.path.exists(output_spool_dir) else 0

            # 将任务信息保存为JSON文件到输出井目录
            task_file_path = os.path.join(output_spool_dir, f'task_{task_id}.json')
            with open(task_file_path, 'w') as f:
                json.dump(task_info, f)

    def clear_output_spool(self):
        """
        清空output_spool文件夹下内容的方法，只删除文件及子文件夹内容，不删除文件夹本身
        """
        if os.path.exists(output_spool_dir):
            for root, dirs, files in os.walk(output_spool_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
            print("output_spool文件夹下内容已清空")
        else:
            print("output_spool文件夹不存在，无需清空")
