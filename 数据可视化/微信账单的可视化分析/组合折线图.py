import pandas as pd
import plotly.express as px

# 从第 17 行(index=16)开始加载数据，将第 16 行(index=15)作为表头
df = pd.read_csv(
    "近一月账单.csv",
    skiprows=16,
    header=0
)

# 过滤无效行
df = df[df["交易时间"].notna() & df["金额(元)"].notna()]

# 处理金额格式：去除 ¥ 符号
df["金额(元)"] = df["金额(元)"].str.replace("¥", "").astype(float)

# 提取日期
df["日期"] = pd.to_datetime(df["交易时间"]).dt.date

# 分别筛选出收入和支出数据
income_df = df[df["收/支"] == "收入"]
expense_df = df[df["收/支"] == "支出"]

# 创建并优化折线图
fig = px.line()

# 添加收入折线
fig.add_scatter(
    x=income_df["日期"],
    y=income_df["金额(元)"],
    mode="lines+markers",
    name="收入",
    marker=dict(size=8, color="#2ca02c", line=dict(width=2, color="white"), symbol="circle"),
    hovertemplate="""<b>日期</b>: %{x}<br><b>收入</b>: %{y:.2f}元"""
)

# 添加支出折线
fig.add_scatter(
    x=expense_df["日期"],
    y=expense_df["金额(元)"],
    mode="lines+markers",
    name="支出",
    marker=dict(size=8, color="#d62728", line=dict(width=2, color="white"), symbol="square"),
    hovertemplate="""<b>日期</b>: %{x}<br><b>支出</b>: %{y:.2f}元"""
)

fig.update_layout(
    title="📅 每日收入和支出趋势",
    xaxis_title="日期",
    yaxis_title="金额（元）",
    plot_bgcolor="white",
    xaxis=dict(tickangle=45, showgrid=True, gridcolor="lightgray"),
    yaxis=dict(showgrid=True, gridcolor="lightgray"),
    height=600,
    width=1000
)

# 显示图表
# fig.show()

# 组合折线图
# fig.write_html("combined_chart.html")

# fig.write_image("组合折线图.png")  # 保存为PNG图片
# 数据量大，不易渲染
