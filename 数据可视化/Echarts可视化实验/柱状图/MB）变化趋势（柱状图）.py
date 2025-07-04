import pandas as pd
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

# 读取 Excel 文件
excel_file = pd.ExcelFile('../实验二数据-1957-2016 (计算机内存价格).xlsx')
df = excel_file.parse('MEMORY', skiprows=4, header=0)

# 获取关键列
year_col = 'X date'
price_col = 'Y $/Mbyte'

# 提取数据并排序
df_clean = df[[year_col, price_col]].dropna().sort_values(by=year_col)

# 过滤价格为0或负值的数据
df_clean = df_clean[df_clean[price_col] > 0]

# 计算价格的统计信息
price_stats = df_clean[price_col].describe()
print(f"价格统计信息:\n{price_stats}")

# 提取处理后的数据
year_data = df_clean[year_col].tolist()
price_data = df_clean[price_col].tolist()


# 智能采样策略 - 根据数据分布动态调整采样密度
def smart_sampling(years, values, max_points=50):
    """智能采样算法，在数据变化剧烈的区域增加采样密度"""
    if len(years) <= max_points:
        return years, values

    # 计算相邻点的变化率
    changes = [abs((values[i + 1] - values[i]) / values[i]) if values[i] > 0 else 0
               for i in range(len(values) - 1)]

    # 按变化率排序，优先保留变化大的点
    sorted_indices = sorted(range(len(changes)), key=lambda i: -changes[i])
    selected_indices = set(sorted_indices[:max_points // 2])  # 保留变化最大的前半部分点

    # 均匀采样剩余的点
    step = len(years) // (max_points - len(selected_indices))
    for i in range(0, len(years), step):
        selected_indices.add(i)

    # 确保首尾点被选中
    selected_indices.add(0)
    selected_indices.add(len(years) - 1)

    # 排序并返回
    selected_indices = sorted(selected_indices)
    return [years[i] for i in selected_indices], [values[i] for i in selected_indices]


# 应用智能采样
sampled_years, sampled_prices = smart_sampling(year_data, price_data)

# 自定义 Y 轴标签格式化函数 - 根据数值大小自动调整单位
yaxis_formatter = JsCode("""
    function(value) {
        if (value >= 1e9) {
            return (value / 1e9).toFixed(2) + 'B';
        } else if (value >= 1e6) {
            return (value / 1e6).toFixed(2) + 'M';
        } else if (value >= 1e3) {
            return (value / 1e3).toFixed(2) + 'K';
        } else if (value >= 1) {
            return value.toFixed(2);
        } else if (value >= 0.01) {
            return value.toFixed(4);
        } else {
            return value.toFixed(6);
        }
    }
""")

# 创建柱状图
bar_chart = (
    Bar()
    .add_xaxis([str(int(y)) for y in sampled_years])
    .add_yaxis(
        "内存价格 ($/MB)",
        sampled_prices,
        color="#ff6666",
        label_opts=opts.LabelOpts(
            is_show=True,
            position="top",
            formatter=JsCode("function(params) { return params.value.toExponential(2); }")
        ),
        itemstyle_opts=opts.ItemStyleOpts(
            opacity=0.8,  # 调整透明度增强立体感
            border_width=0.5,
            border_color="#333"
        ),
        tooltip_opts=opts.TooltipOpts(
            formatter="{b}年<br/>价格：{c} $/MB"
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="1957-2016年内存价格变化趋势（优化版柱状图）",
            subtitle="数据来源：实验二数据-计算机内存价格"
        ),
        xaxis_opts=opts.AxisOpts(
            name="年份",
            type_="category",
            axislabel_opts=opts.LabelOpts(
                rotate=45,
                interval="auto",
                font_size=9
            ),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=1)
            )
        ),
        yaxis_opts=opts.AxisOpts(
            name="价格 ($/MB)",
            type_="log",  # 使用对数轴处理大范围数据
            min_=0.0001,  # 进一步调整最小值
            max_=1e9,  # 最大值保持10亿
            axislabel_opts=opts.LabelOpts(
                formatter=yaxis_formatter  # 使用自定义格式化函数
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(width=0.5, opacity=0.5)
            )
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="shadow",
            formatter="{b}年<br/>价格：{c} $/MB"
        ),
        toolbox_opts=opts.ToolboxOpts(
            is_show=True,
            feature={
                "dataZoom": {"yAxisIndex": "none"},
                "restore": {},
                "saveAsImage": {"type": "png", "title": "保存为图片"}
            }
        ),
        datazoom_opts=[
            opts.DataZoomOpts(type_="slider", xaxis_index=0),
            opts.DataZoomOpts(type_="inside", xaxis_index=0)
        ],
        legend_opts=opts.LegendOpts(
            pos_top="5%",
            pos_right="5%"
        )
    )
)

# 生成 HTML 文件
bar_chart.render("memory_price_optimized.html")
print("\n🎉 优化版图表已成功生成：memory_price_optimized.html")
print("请在浏览器中打开该文件查看图表")