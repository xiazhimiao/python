import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取Excel数据
data = pd.read_excel('../Python数据文件.xls')

# 筛选出男生的数据
male_data = data[data['性别'] == '男']

# 获取男生身高数据
heights = male_data['身高']

# 绘制直方图
plt.hist(heights, bins='auto', density=True, alpha=0.75, edgecolor='black')

# 计算拟合曲线参数
mu, std = norm.fit(heights)
x = np.linspace(min(heights), max(heights), 100)
pdf = norm.pdf(x, mu, std)

# 绘制拟合曲线
plt.plot(x, pdf, 'k-', linewidth=2)

# 添加标题和坐标轴标签
plt.title('男生身高分布')
plt.xlabel('身高')
plt.ylabel('频数')

# 显示图形
plt.show()