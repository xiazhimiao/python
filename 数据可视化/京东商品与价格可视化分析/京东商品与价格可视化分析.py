from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
import pandas as pd
import yaml

df = pd.read_csv('../../京东/new_file_cp.csv', usecols=['price', 'comments'])

# 假设数据已经读取到 df 中
# 先去除字符串中的货币符号，再将其转换为浮点数
df['price'] = df['price'].str.replace('￥', '').astype(float)


# 对价格列进行排序
# df_sorted0 = df.sort_values(by='price')


# 假设数据已经读取到 df 中
# 提取数字部分并转换为整数
def extract_number(text):
    if text == '0条评论':
        return 0
    if '+' in text:
        number_part = text.split('+')[0]
    else:
        number_part = text.split('条')[0]
    if '万' in number_part:
        return int(float(number_part.replace('万', '')) * 10000)
    else:
        try:
            return int(number_part)
        except ValueError:
            return 0


df['comments_num'] = df['comments'].apply(extract_number)

# 对评论数量列进行排序
# df_sorted1 = df.sort_values(by='comments_num')


# 构成字典
data_dict = dict(zip(df['price'].tolist(), df['comments_num'].tolist()))
# 字典排序返回列表套元组
sorted_data = sorted(data_dict.items(), key=lambda item: item[0])
# 生成列表
price = [t[0] for t in sorted_data]
comments = [t[1] for t in sorted_data]

c = (
    Bar()
    .add_xaxis(price)
    .add_yaxis("评论数", comments)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="京东搜索商品价格与评论柱状图"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    .render("Price与Comments.html")
)
# print(Faker.days_attrs)
# print(Faker.days_values)


# 将字典写入 YAML 文件
with open('data.yml', 'w') as f:
    yaml.dump(data_dict, f)
