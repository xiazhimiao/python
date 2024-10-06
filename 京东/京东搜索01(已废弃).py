import urllib
import re
import json
import requests
import pandas as pd
import time

keyword = "计算机"
start_url = "https://re.jd.com/search?keyword=" + urllib.parse.quote_plus(keyword)


# print(start_url)

# 获取网页源码
def get_html_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding  # 将响应对象的编码设置为通过分析响应内容推断出的编码,较为准确
        return r.text
    except:
        return ""


# 提取json内容
def extract(text):
    pattern = r'var pageData = ({.*?});'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_data_str = match.group(1)
        try:
            json_data = json.loads(json_data_str)
            result_content = json_data.get('result', [])
            page_count = json_data.get('summary').get('pagecount')

            return [result_content, page_count]
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"
    else:
        return "No JSON data found."


def while_page_count(page_count, file_name):
    page = 2
    while page_count - 1:
        start_time = time.time()

        url = "https://re.jd.com/search?keyword=" + urllib.parse.quote_plus(keyword) + "&page=" + str(page)
        # 入口创建文件
        existing_df = pd.read_csv(file_name)
        # 新的数据

        try:
            data0 = extract(get_html_text(url))[0]
            new_data = pd.DataFrame(data0)
            combined_df = pd.concat([existing_df, new_data], ignore_index=True)
            combined_df.to_csv(file_name, index=False)
            page += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"循环第{page - 1}次耗时：{elapsed_time:.5f}秒")
        except ValueError as e:
            print(f"第{page - 1}次循环失败{e}")
            continue
            # 可以在这里添加一些错误处理的逻辑，比如返回一个默认的 DataFrame 或者采取其他补救措施
            # new_data = pd.DataFrame()
# while data:
#     print(f"循环第{page}次请求失败重新请求")
#     data = extract(get_html_text(url))[0]


# if not data0:
#     for i in range(3):
#         print(f"循环第{page}次请求失败重新请求,第{i+1}次")
#         data0 = extract(get_html_text(url))[0]
#         if data0:
#             continue


if __name__ == '__main__':
    # print(extract(get_html_text(start_url)))
    data = extract(get_html_text(start_url))[0]
    page_count = extract(get_html_text(start_url))[1]
    file_name = keyword + '.csv'
    print('总页数:' + str(page_count))
    # print(data[0].get('ad_title', []))
    # print(page_count)
    # with open('jd.json', 'w', encoding='utf-8') as f:
    #     f.write(data)
    try:
     df = pd.DataFrame(data)
     df.to_csv(file_name, index=False)

     # # 创建一个空的 DataFrame
     # df = pd.DataFrame()
     #
     # # 保存为 CSV 文件
     # df.to_csv(file_name, index=False)

     while_page_count(page_count, file_name)
    except ValueError as e:
        print(e)
        print('目前这个接口不能使用')


