import urllib
import re
import json
import requests
import pandas as pd
import time




# print(start_url)

# 获取网页源码
def get_html_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        'cookie':'__jdu=1727785786646135020273; shshshfpa=b45bc713-dc47-9ebb-bd18-9fb594d45a09-1727785787; shshshfpx=b45bc713-dc47-9ebb-bd18-9fb594d45a09-1727785787; _reuuid=d2805fd02a8c4da29b923c8eddfe0ab4; ipLoc-djd=9-644-24071-61762; TrackID=1QPYen_klaDwGsVlITLOeqXy4fTuwgFMlzGoYa3RQEkw_nOfQMc09wC6lb8_SAefQJFKBk8TLXUz4O91okPwbPsld824PV1_e9R_GM7ZnNOjPuBGLtZAVuCJYbKwHxyhi; thor=17EADF3219C054D0F8F724A13FAED3FC03500126A377D70E1854D4BE280C72BD0533DDB73C6B1F04F4B3C2C1D75D9D53F11B614779E7565FAF4D1D7AE71EE5077CCD3D048E6FD5E58CA4350DC4B12C1EC9B7D418E4D71F8C7C212B5477B486CCF37E0C54A01424C9EF8284CC9414175658776B90D5FC7C51500D7BC2CBB69813A133322F4EE9F743B2BF50E70705336BE8EAA02AA2B1E488B68AC3FDF16D7974; light_key=AASBKE7rOxgWQziEhC_QY6yaSMG0mKMYn8pZ1CBvAT3n-PzKKc8rqB-wu0PxLJ8SO4UaBdTQ; pinId=1sgNBwwgQZg3AnK5R2l_dA; pin=jd_cMJEcaoiMzXP; unick=jd_tsv801e3l8oi43; _tp=%2BpBenPUVKZf6tg8PGzM0%2Fg%3D%3D; _pst=jd_cMJEcaoiMzXP; unpl=JF8EALJnNSttXENQAhtRGBIXSF1SWw0BQx4Lb28DVVoITFwAGwMeFEd7XlVdWBRLFh9uYBRUXlNJVg4fBCsSEXteU11bD00VB2xXVgQFDQ8WUUtBSUt-S1tXV1QOSh4AbGYDZG1bS2QFGjIbFBNNW11aWwFMEAZoZwdQXFtKVwMZMhoiF3ttZF1cDEkTBF9mNVVtGh8IDB0KGxMVBl1SXVsOQhMFZmACUVpYSVAEGAMYFBJ7XGRd; __jdv=76161171|direct|-|none|-|1729516648705; 3AB9D23F7A4B3CSS=jdd03VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4AAAAMSV444ICAAAAAACOSEKZNVWESBGQX; flash=3_rZSbUaCKsFzIG3zEfk6KK-lkpoHh93zEttxov67-8d8zRXes0Dd_lng527cxIHQv0KVKBp28JbP5gWSTDRSalI7U1PVq9Vf5ZbrpXlSLsGGDctzKyHxbVeUj7kkqV73YfhoSUr82yJKhewfgM1xcY916-QU8KjjQaJhF6sSTpl1vRAjF8d4-; PCSYCityID=CN_220000_220200_0; shshshfpb=BApXSpXUxrPdArWkDLgBwDw_R9sIvEuvTBmU5UKhs9xJ1MofQ5oC2; __jda=229668127.1727785786646135020273.1727785787.1728470438.1729516649.8; areaId=9; ipLoc-djd=9-644-0-0; __jdb=229668127.3.1727785786646135020273|8.1729516649; 3AB9D23F7A4B3C9B=VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4'
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
    # while page_count - 1:
    for _ in range(page_count - 1):
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
            page += 1
            print(f"第{page}次循环失败{e}")
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

    keyword = "计算机"
    start_url = "https://re.jd.com/search?keyword=" + urllib.parse.quote_plus(keyword)

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


