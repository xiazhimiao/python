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

# 创建包含两个子图的图表
fig = plt.figure(figsize=(16, 12))

# 第一个子图：男女生身高条形图
ax1 = fig.add_subplot(2, 1, 1)  # 2行1列的第一个子图

bar_width = 0.35
index = np.arange(len(avg_height_by_constellation.index))
bar1 = ax1.bar(index - bar_width / 2, avg_height_by_constellation['男'],
              bar_width, label='男生', color='skyblue')
bar2 = ax1.bar(index + bar_width / 2, avg_height_by_constellation['女'],
              bar_width, label='女生', color='lightcoral')

# 添加标题和标签
ax1.set_title('不同星座男女生平均身高排行')
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

# 第二个子图：女生身高直方图和拟合曲线
ax2 = fig.add_subplot(2, 1, 2)  # 2行1列的第二个子图

# 绘制女生身高直方图
n, bins, patches = ax2.hist(female_heights, bins='auto', density=True, alpha=0.3,
                           color='lightcoral', edgecolor='black', label='身高分布')

# 拟合正态分布曲线
mu, sigma = norm.fit(female_heights)
x = np.linspace(female_heights.min(), female_heights.max(), 100)
p = norm.pdf(x, mu, sigma)
ax2.plot(x, p, 'r-', linewidth=2, label=f'正态分布拟合 (μ={mu:.2f}, σ={sigma:.2f})')
ax2.fill_between(x, p, alpha=0.1, color='red')

# 添加标题和标签
ax2.set_title('女生身高分布拟合曲线')
ax2.set_xlabel('身高(cm)')
ax2.set_ylabel('密度')
ax2.legend(loc='upper left')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# 调整整体布局
plt.tight_layout()
plt.show()