import pandas as pd
import plotly.express as px

# ====================== 数据加载与清洗 ======================
df = pd.read_csv(
    "近一月账单.csv",
    skiprows=16,
    header=0
)
df = df[df["交易时间"].notna() & df["金额(元)"].notna()]
df["金额(元)"] = df["金额(元)"].str.replace("¥", "").astype(float)

# 支出取绝对值，统一为正数以便展示占比（收入/支出均视为金额流动）
df["金额(元)"] = df["金额(元)"].abs()

# ====================== 数据分组与统计 ======================
type_summary = df.groupby("交易类型")["金额(元)"].sum().reset_index()
type_summary = type_summary.sort_values("金额(元)", ascending=False)  # 按金额降序排列

# ====================== 绘制饼图 ======================
fig = px.pie(
    type_summary,
    values="金额(元)",
    names="交易类型",
    title="🎖 交易类型金额占比",
    color_discrete_sequence=[  # 自定义颜色（与堆积柱状图保持一致）
        "#ff9966",  # 商户消费-橙色
        "#66c2ff",  # 扫码付款-蓝色
        "#9966ff",  # 转账-紫色
        "#ffcc99",  # 其他-浅橙色
        "#808080"  # 中性交易-灰色
    ],
    hole=0.4,  # 圆心镂空显示总金额
    height=600,
    width=800
)

# 添加圆心总金额文本
total_amount = df["金额(元)"].sum()
fig.add_annotation(
    x=0.5, y=0.5,
    text=f"总金额<br>¥{total_amount:.2f}",
    font=dict(size=16, color="darkblue"),
    showarrow=False
)

# 优化标签格式（显示百分比，保留1位小数）
fig.update_traces(
    textinfo="percent+label",  # 标签显示百分比和类型名称
    textposition="outside",  # 标签位于扇形外侧
    hovertemplate="""<b>交易类型</b>: %{label}<br><b>金额</b>: ¥%{value:.2f}<br><b>占比</b>: %{percent:.1%}"""
)

# 显示图表
# fig.show()

# 交易类型饼图
# fig.write_html("pie_chart.html")

# fig.write_image("交易类型饼图.png")  # 保存为PNG图片
# 数据量大，不易渲染
