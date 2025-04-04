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

# 处理金额格式：支出为负，收入为正
df["金额(元)"] = df["金额(元)"].str.replace("¥", "").astype(float)
df["金额(元)"] = df.apply(lambda row: -row["金额(元)"] if row["收/支"] == "支出" else row["金额(元)"], axis=1)

# 提取日期
df["日期"] = pd.to_datetime(df["交易时间"]).dt.date

# 按日期分组计算净收支
daily_summary = df.groupby("日期")["金额(元)"].sum().reset_index()

# 创建并优化折线图
fig = px.line(
    daily_summary,
    x="日期",
    y="金额(元)",
    title="📅 每日净收支趋势（收入为正，支出为负）",
    labels={"日期": "日期", "金额(元)": "净收支金额（元）"},
    height=600,
    width=1000
)

fig.update_layout(
    plot_bgcolor="white",
    xaxis=dict(tickangle=45, showgrid=True, gridcolor="lightgray"),
    yaxis=dict(showgrid=True, gridcolor="lightgray")
)

fig.update_traces(
    mode="lines+markers",
    marker=dict(size=8, color="#1f77b4", line=dict(width=2, color="white")),
    hovertemplate="""<b>日期</b>: %{x}<br><b>净收支</b>: %{y:.2f}元"""
)

# 显示图表
# fig.show()

# 净收入折线图
# fig.write_html("net_income_chart.html")

# fig.write_image("净收入.png")  # 保存为PNG图片
# 数据量大，不易渲染
