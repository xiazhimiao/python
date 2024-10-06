import requests
from urllib.parse import quote

# https://re.jd.com/search?keyword=%E8%8B%B9%E6%9E%9C&page=3
# https://re.jd.com/search?keyword=%E8%8B%B9%E6%9E%9C&page=1

url = 'https://re.jd.com/search'

data = input("<京东>：//请输入要搜索的内容：\n")
# 进行url编码
data = quote(data)

params = {'keyword': data, 'enc': 'utf-8'}
# headers = {
#     'user-agent':
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
#     'cookie':
#         'ipLoc-djd=9-644-0-0; jsavif=1; jsavif=1; 3AB9D23F7A4B3CSS=jdd03VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4AAAAMSJAHNXMQAAAAAD5G5BSYLFHEA2MX; _gia_d=1; xapieid=jdd03VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4AAAAMSJAHNXMQAAAAAD5G5BSYLFHEA2MX; __jda=143920055.1727785786646135020273.1727785787.1727785787.1727785787.1; __jdc=143920055; __jdv=143920055|localhost:63342|-|referral|-|1727785786647; __jdu=1727785786646135020273; shshshfpa=b45bc713-dc47-9ebb-bd18-9fb594d45a09-1727785787; shshshfpx=b45bc713-dc47-9ebb-bd18-9fb594d45a09-1727785787; rkv=1.0; areaId=9; __jdb=143920055.2.1727785786646135020273|1.1727785787; qrsc=2; shshshfpb=BApXSc2sGS_dArWkDLgBwDw_R9sIvEuvTBmU5UKho9xJ1MofQ5oC2; 3AB9D23F7A4B3C9B=VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4'
# }


# resp = requests.get(url, params=params, headers=headers)
resp = requests.get(url, params=params)
resp.encoding = 'utf-8'
# print(resp.text)

# with open("jd.html", "w", encoding='utf-8') as f:
#     f.write(resp.text)
print(resp.request.url)