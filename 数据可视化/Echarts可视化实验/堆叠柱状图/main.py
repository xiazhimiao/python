import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

# 文件路径（根据实际情况调整）
file_path = '../实验二数据-1957-2016 (计算机内存价格).xlsx'

try:
    # 读取Excel文件
    excel_file = pd.ExcelFile(file_path)

    # 读取DDRIVES表（表头在第5行，索引4）
    ddrives_df = excel_file.parse('DDRIVES', header=4)
    # 读取SSD表（表头在第4行，索引3）
    ssd_df = excel_file.parse('SSD', header=3)

    # 处理DDRIVES数据：筛选2013-2016年，计算$/GB（Size Mbytes转换为GB）
    ddrives_df = ddrives_df[(ddrives_df['Year'] >= 2013) & (ddrives_df['Year'] <= 2016)]
    ddrives_df['price_per_gb'] = ddrives_df['Cost US$'] / (ddrives_df['Size Mbytes'] / 1024)
    ddrives_yearly = ddrives_df.groupby('Year')['price_per_gb'].mean().reset_index()

    # 处理SSD数据：筛选2013-2016年，计算$/GB（Effective Size Mbytes转换为GB）
    ssd_df = ssd_df[(ssd_df['Year'] >= 2013) & (ssd_df['Year'] <= 2016)]
    ssd_df['price_per_gb'] = ssd_df['(include shipping) Cost $US'] / (ssd_df['Effective Size Mbytes'] / 1024)
    ssd_yearly = ssd_df.groupby('Year')['price_per_gb'].mean().reset_index()

    # 合并数据
    merged_data = pd.merge(ddrives_yearly, ssd_yearly, on='Year', suffixes=('_dd', '_ssd'))

    # 绘制堆叠柱状图
    bar_chart = (
        Bar()
        .add_xaxis(merged_data['Year'].astype(str).tolist())
        .add_yaxis(
            "机械硬盘（DDRIVES）",
            merged_data['price_per_gb_dd'].tolist(),
            stack="价格堆叠"
        )
        .add_yaxis(
            "SSD",
            merged_data['price_per_gb_ssd'].tolist(),
            stack="价格堆叠"
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="2013-2016年SSD与机械硬盘价格变化趋势（$/GB）",
                pos_top="5px",  # 标题上移
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_size=14)  # 调整字体大小
            ),
            legend_opts=opts.LegendOpts(pos_top="30px"),  # 图例上移，避免遮挡
            xaxis_opts=opts.AxisOpts(
                name="年份",
                axislabel_opts=opts.LabelOpts(margin=15)  # 增加标签与轴线的距离
            ),
            yaxis_opts=opts.AxisOpts(
                name="价格（$/GB）",
                axislabel_opts=opts.LabelOpts(margin=15)  # 增加标签与轴线的距离
            )
        )
    )

    # 渲染图表
    bar_chart.render("ssd_ddrives_price_trend.html")
    print("图表已成功生成：ssd_ddrives_price_trend.html")

except FileNotFoundError:
    print(f"错误：未找到文件 '{file_path}'，请检查路径是否正确")
except KeyError as ke:
    print(f"键错误：找不到列 '{ke}'，请检查列名是否正确")
except Exception as e:
    print(f"发生未知错误：{e}")