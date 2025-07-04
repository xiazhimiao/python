import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 星座映射字典
constellation_mapping = {
    "白羊": "白羊座", "金牛": "金牛座", "双子": "双子座",
    "巨蟹": "巨蟹座", "狮子": "狮子座", "处女": "处女座",
    "天秤": "天秤座", "天蝎": "天蝎座", "射手": "射手座",
    "摩羯": "摩羯座", "水瓶": "水瓶座", "双鱼": "双鱼座"
}

# 读取数据并预处理星座
data = pd.read_excel('../Python数据文件.xls')
data['星座'] = data['星座'].apply(lambda x: constellation_mapping.get(x, x))

# 按星座和性别分组计算平均身高
avg_height_by_constellation = data.groupby(['星座', '性别'])['身高'].mean().unstack()
# 排序（按女生平均身高降序）
avg_height_by_constellation = avg_height_by_constellation.sort_values(by='女', ascending=False)

# 提取女生身高数据用于拟合曲线
female_data = data[data['性别'] == '女']
female_heights = female_data['身高']

# 创建图表和共享x轴的双Y坐标轴
fig, ax1 = plt.subplots(figsize=(16, 10))
ax2 = ax1.twinx()  # 创建共享x轴的第二个Y轴

# 绘制男女生身高条形图
bar_width = 0.35
index = np.arange(len(avg_height_by_constellation.index))
# 使用蓝色表示男生
bar1 = ax1.bar(index - bar_width / 2, avg_height_by_constellation['男'],
              bar_width, label='男生', color='#1f77b4')  # 蓝色
# 使用红色表示女生
bar2 = ax1.bar(index + bar_width / 2, avg_height_by_constellation['女'],
              bar_width, label='女生', color='#d62728')  # 红色

# 添加标题和标签
ax1.set_title('不同星座男女生平均身高排行及女生身高分布拟合曲线')
ax1.set_xlabel('星座')
ax1.set_ylabel('平均身高(cm)')
ax1.set_xticks(index)
ax1.set_xticklabels(avg_height_by_constellation.index, rotation=45)
ax1.legend(loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 添加数值标签
for bar in ax1.patches:
    height = bar.get_height()
    ax1.annotate(f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords='offset points',
                ha='center', va='bottom')

# 计算星座位置到身高的映射关系
height_min = female_heights.min()
height_max = female_heights.max()
x_positions = np.linspace(0, len(avg_height_by_constellation.index)-1, 100)

# 将身高数据归一化到星座位置范围
def height_to_position(height):
    return ((height - height_min) / (height_max - height_min)) * (len(avg_height_by_constellation.index)-1)

# 绘制女生身高直方图和拟合曲线
# 使用归一化后的身高位置
positions = [height_to_position(h) for h in female_heights]

# 调整直方图的bins使其与星座位置对应
# 使用绿色表示身高分布
n, bins, patches = ax2.hist(positions, bins=len(avg_height_by_constellation.index),
                           density=True, alpha=0.5, color='#2ca02c',  # 绿色
                           edgecolor='black', label='身高分布')

# 拟合正态分布曲线（在位置空间）
mu_position = height_to_position(np.mean(female_heights))
sigma_position = (height_to_position(np.mean(female_heights) + np.std(female_heights)) -
                 height_to_position(np.mean(female_heights)))

# 生成位置空间的正态分布曲线
# 使用深绿色表示拟合曲线
p_position = norm.pdf(x_positions, mu_position, sigma_position)
ax2.plot(x_positions, p_position, '-', linewidth=2,
        label=f'正态分布拟合 (μ={np.mean(female_heights):.2f}cm, σ={np.std(female_heights):.2f}cm)',
        color='#17701a')  # 深绿色
ax2.fill_between(x_positions, p_position, alpha=0.1, color='#2ca02c')  # 绿色

# 设置第二个Y轴标签
ax2.set_ylabel('概率密度')

# 添加星座区域分隔线
for i in range(len(avg_height_by_constellation.index)):
    ax2.axvline(x=i, color='gray', linestyle='--', alpha=0.3)

# 为第二个Y轴添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

# 调整布局
plt.tight_layout()
plt.show()