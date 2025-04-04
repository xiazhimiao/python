import requests

url = 'https://www.runoob.com/'

# 菜鸟服务端并不会验证UA信息
response = requests.get(url)

response.encoding = 'utf-8'

# print(response.text)

with open('cainiao1.html', 'wb') as f:
    f.write(response.content)
























with open('cainiao2.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
    # response.text 根据指定或者默认的编码进行翻译的文本数据
    # 在获取这个属性之前需要指定编码,否则可能出现写入'错误'

# 这里不论是以二进制序列写入还是以指定编码的文本方式写入都没问题
# 但,需要注意的是,文本写入是以指定的编码进行翻译文本为二进制序列写入,如果指定错误,那么写入的序列在本应指定的文本编辑器就会出现乱码
