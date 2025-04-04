import pandas as pd
import plotly.express as px

# ====================== 数据加载与清洗 ======================
# 从第 17 行开始读取数据（根据微信账单格式调整，假设前16行为说明）
df = pd.read_csv(
    "近一月账单.csv",
    skiprows=16,
    header=0
)

# 过滤无效行（交易时间和金额非空）
df = df[df["交易时间"].notna() & df["金额(元)"].notna()]

# 处理金额格式：去除¥符号并转换为数值
df["金额(元)"] = df["金额(元)"].str.replace("¥", "").astype(float)

# 提取日期（仅日期部分，去除时间）
df["日期"] = pd.to_datetime(df["交易时间"]).dt.date

# ====================== 数据分组与统计 ======================
# 按日期和交易类型分组，计算金额总和
daily_type_summary = df.groupby(["日期", "交易类型"])["金额(元)"].sum().reset_index()

# ====================== 绘制分类堆积柱状图 ======================
fig = px.bar(
    daily_type_summary,
    x="日期",
    y="金额(元)",
    color="交易类型",  # 按交易类型分色
    title="📊 每日不同交易类型收支分布",
    labels={
        "日期": "日期",
        "金额(元)": "金额（元）",
        "交易类型": "交易类型"
    },
    height=600,
    width=1000
)

# 优化图表布局
fig.update_layout(
    plot_bgcolor="white",  # 背景色
    xaxis=dict(
        tickangle=45,  # 日期标签倾斜45度避免重叠
        showgrid=True,  # 显示网格线
        gridcolor="lightgray"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="lightgray"
    ),
    legend=dict(title="交易类型", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)  # 图例位置
)

# 显示图表
# fig.show()

# 分类堆积柱状图
# fig.write_html("stacked_bar_chart.html")

# fig.write_image("分类堆积柱状图.png")  # 保存为PNG图片
# 数据量大，不易渲染
