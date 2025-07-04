import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体（保留SimHei并添加备用字体）
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 确保负号正确显示

# 读取Excel数据
data = pd.read_excel('../Python数据文件.xls')

# 数据探查
print("数据基本情况：")
data.info()

# 按省份和性别统计人数
counts = data.groupby(['籍贯', '性别']).size().unstack()

# 填充缺失值为0（关键修改点）
counts = counts.fillna(0)

# 输出分组统计结果
print("分组统计结果：")
print(counts)
print(f"统计结果行数：{len(counts)}")

# 设置柱形宽度
bar_width = 0.35
r1 = np.arange(len(counts.index))
r2 = [x + bar_width for x in r1]

# 绘制柱形图
plt.figure(figsize=(15, 8))  # 增大图表尺寸
plt.bar(r1, counts['男'], width=bar_width, label='男', color='gray')
plt.bar(r2, counts['女'], width=bar_width, label='女', color='white', edgecolor='black')

# 添加标题和坐标轴标签
plt.title('各省、市、自治区的人数分布')
plt.xlabel('籍贯')
plt.ylabel('人数')

# 设置x轴刻度标签，旋转90度避免重叠
plt.xticks([r + bar_width/2 for r in r1], counts.index, rotation=90)

# 添加图例和网格线
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()