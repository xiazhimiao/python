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

# 分离收入和支出数据
income_df = df[df["收/支"] == "收入"].sort_values("日期")  # 收入数据按日期排序
expense_df = df[df["收/支"] == "支出"].sort_values("日期")  # 支出数据按日期排序

# ====================== 计算累计值 ======================
# 累计收入（从第一天到当前日期的收入总和）
income_df["累计收入"] = income_df["金额(元)"].cumsum()
# 累计支出（从第一天到当前日期的支出总和，支出本身为负数，此处取绝对值展示累计消耗）
expense_df["累计支出"] = expense_df["金额(元)"].abs().cumsum()  # 支出金额取绝对值后累计

# ====================== 绘制累计折线图 ======================
fig = px.line()

# 添加累计收入折线
fig.add_scatter(
    x=income_df["日期"],
    y=income_df["累计收入"],
    mode="lines+markers",
    name="累计收入",
    marker=dict(size=8, color="#2ca02c", line=dict(width=2, color="white")),  # 绿色系
    hovertemplate="""<b>日期</b>: %{x}<br><b>累计收入</b>: %{y:.2f}元""",
    fill='tozeroy',  # 填充到Y轴零点
    fillcolor='rgba(44, 160, 44, 0.2)'  # 浅绿色半透明填充

)

# 添加累计支出折线
fig.add_scatter(
    x=expense_df["日期"],
    y=expense_df["累计支出"],
    mode="lines+markers",
    name="累计支出",
    marker=dict(size=8, color="#d62728", line=dict(width=2, color="white")),  # 红色系
    hovertemplate="""<b>日期</b>: %{x}<br><b>累计支出</b>: %{y:.2f}元""",
    fill='tozeroy',  # 填充到Y轴零点
    fillcolor='rgba(214, 39, 40, 0.2)'  # 浅红色半透明填充
)

# 优化图表布局
fig.update_layout(
    title="📈 累计收入与支出趋势",
    xaxis_title="日期",
    yaxis_title="累计金额（元）",
    plot_bgcolor="white",
    xaxis=dict(
        tickangle=45,
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="lightgray"
    ),
    height=600,
    width=1000
)

# 显示图表
# fig.show()

# 累计折线图
# fig.write_html("cumulative_chart.html")

# fig.write_image("累计折线图.png")  # 保存为PNG图片
# 数据量大，不易渲染
