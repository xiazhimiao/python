import pandas as pd
from pyecharts.charts import Pie, Timeline
from pyecharts import options as opts

# 读取Excel文件，表头在第5行（索引4）
try:
    df = pd.read_excel('实验二数据-1957-2016 (计算机内存价格).xlsx', sheet_name='DDRIVES', header=4)
except Exception as e:
    print(f"读取文件失败: {e}")
    exit(1)

# 数据探查
print("\n数据列名：", df.columns.tolist())
print("\n前5行数据：\n", df.head())

# 定义关键列
year_col = 'Year'
man_col = 'Manufacturer'

# 数据预处理：筛选2000-2016年，转换年份为数值
df_filtered = df[
    df[year_col].between(2000, 2016) &
    df[year_col].notna()
    ].copy()
df_filtered[year_col] = df_filtered[year_col].astype(int)

# 数据清洗：统一厂家名称（纠正拼写错误）
manufacturer_mapping = {
    "Western Digital Corp": "Western Digital",
    "Western Digital Corporation": "Western Digital",
    "Western Digital Technologies": "Western Digital",
    "Westgtern Digital": "Western Digital",
    "Westgrn Digital": "Western Digital",
    "HGST (Hitachi)": "Hitachi",
    "Hitachi GST": "Hitachi",
    "Hitachi Global Storage Technologies": "Hitachi",
    "Seagate Technology": "Seagate",
    "Seagate Technology LLC": "Seagate",
    "Samsung Electronics": "Samsung",
    "Samsung Electronics Co., Ltd.": "Samsung",
    "Toshiba Corp": "Toshiba",
    "Toshiba Corporation": "Toshiba",
    "IBM Corporation": "IBM",
    "Fujitsu Limited": "Fujitsu",
    "Maxtor Corporation": "Maxtor",
    "Micropolis MC1528-15": "Micropolis",
    "n/a": "Unknown",
    "nan": "Unknown",
    "": "Unknown",
    None: "Unknown"
}

# 应用映射统一厂家名称
df_filtered[man_col] = df_filtered[man_col].astype(str).apply(
    lambda x: manufacturer_mapping.get(x.strip(), x.strip())
)

# 创建时间轴
timeline = Timeline(init_opts=opts.InitOpts(width="1600px", height="900px"))

# 设置更丰富的颜色方案（20种颜色）
pie_colors = [
    "#37A2DA", "#32C5E9", "#67E0E3", "#9FE6B8", "#FFDB5C",
    "#ff9f7f", "#fb7293", "#E062AE", "#E690D1", "#e7bcf3",
    "#9d96f5", "#8378EA", "#96BFFF", "#00BFFF", "#1E90FF",
    "#6495ED", "#4682B4", "#20B2AA", "#3CB371", "#2E8B57"
]

# 按年份生成饼图
for year in range(2000, 2017):
    df_year = df_filtered[df_filtered[year_col] == year]
    manufacturer_counts = df_year[man_col].value_counts().reset_index()
    manufacturer_counts.columns = ['厂家', '数量']

    # 只显示数量大于0的厂家
    manufacturer_counts = manufacturer_counts[manufacturer_counts['数量'] > 0]

    pie = (
        Pie()
        .add(
            series_name="市场份额",
            data_pair=[list(z) for z in zip(manufacturer_counts['厂家'], manufacturer_counts['数量'])],
            radius=["30%", "70%"],
            color=pie_colors,
            label_opts=opts.LabelOpts(
                formatter="{b}: {d}% ({c}个)",
                font_size=12,
                position="outside",
                background_color="rgba(255,255,255,0.8)",
                border_color="#aaa",
                border_width=1,
                padding=[2, 4],
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{year}年硬盘生产厂家市场份额分布",
                subtitle=f"共{len(df_year)}个产品记录，{len(manufacturer_counts)}个厂家",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_size=24),  # 修正为TitleOpts的正确参数
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_top="10%",
                pos_left="2%",
                type_="scroll",
                item_width=14,
                item_height=14,
                textstyle_opts=opts.TextStyleOpts(  # 修正为正确的参数名
                    font_size=12,
                    color="#333",
                    font_family="SimHei"
                ),
            ),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                orient="vertical",
                pos_top="center",
                pos_right="2%",
                feature={
                    "saveAsImage": {},
                    "dataView": {"readOnly": False},
                    "restore": {},
                    "magicType": {"type": ["pie", "rose"]},
                }
            )
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="{a} <br/>{b}: {c}个产品 ({d}%)",
                background_color="rgba(255,255,255,0.9)",
                border_color="#ccc",
                border_width=1,
                textstyle_opts=opts.TextStyleOpts(  # 修正为正确的参数名
                    color="#333",
                    font_size=12
                ),
            )
        )
    )
    timeline.add(pie, time_point=str(year))

# 时间轴配置
timeline.add_schema(
    play_interval=1500,
    is_auto_play=True,
    is_loop_play=True,
    is_rewind_play=True,
    label_opts=opts.LabelOpts(
        font_size=14,
    ),
)

# 生成HTML
timeline.render("硬盘厂家变化.html")
print("图表生成成功，查看硬盘厂家变化.html")