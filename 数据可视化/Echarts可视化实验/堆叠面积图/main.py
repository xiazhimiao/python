import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

# 文件路径
file_path = '../实验二数据-1957-2016 (计算机内存价格).xlsx'

try:
    # 读取FLASH表
    flash_df = pd.read_excel(file_path, sheet_name='FLASH', header=3)

    # 筛选2003-2016年数据
    flash_df = flash_df[(flash_df['Year'] >= 2003) & (flash_df['Year'] <= 2016)]

    # 计算容量（GB）
    flash_df['Size_GB'] = flash_df['Size Mbytes'] / 1024

    # 定义容量区间
    bins = [0, 10, 50, 100, 500, float('inf')]
    labels = ['0-10GB', '10-50GB', '50-100GB', '100-500GB', '>500GB']
    flash_df['Size_Group'] = pd.cut(flash_df['Size_GB'], bins=bins, labels=labels)

    # 分组统计时指定 observed=False（消除警告）
    grouped = flash_df.groupby(['Year', 'Size_Group'], observed=False).size().unstack(fill_value=0)

    # 创建折线图（面积填充）
    line = Line()
    line.add_xaxis(grouped.index.astype(str).tolist())

    for col in grouped.columns:
        line.add_yaxis(
            series_name=col,
            y_axis=grouped[col].tolist(),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            stack="总量",
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )

    # 全局配置
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="2003-2016年FLASH存储设备容量分布趋势"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="产品数量"),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            formatter="{b}<br/>{c}件"
        ),
        legend_opts=opts.LegendOpts(pos_top="5%", pos_left="center"),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )

    # 渲染图表
    line.render("flash_capacity_area_chart.html")
    print("图表已生成：flash_capacity_area_chart.html")

except FileNotFoundError:
    print("文件未找到，请检查路径")
except KeyError as ke:
    print(f"列名错误：{ke}")
except Exception as e:
    print(f"未知错误：{e}")