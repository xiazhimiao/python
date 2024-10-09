import unittest
import re
import requests
import yaml
from bs4 import BeautifulSoup
import html2text

# 获取网页源码
def get_html_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'cookie': 'ff54ff0fa0f557568e6e69d35b815894=fcad32351f41e0bacbc3c4dc74b2a721; zh_choose=n; _ga=GA1.1.234751423.1728474308; _ga_YN9485YEKE=GS1.1.1728476768.2.0.1728476768.0.0.0'
    }
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding  # 将响应对象的编码设置为通过分析响应内容推断出的编码,较为准确
        return r.text
    except:
        return ""


def fetch_and_save_urls(url):
    html = get_html_text(url)
    soup = BeautifulSoup(html, 'html.parser')
    ul_tag = soup.find('ul', class_='chaw_c')
    a_all = ul_tag.find_all('a')
    urls = []
    for a in a_all:
        a_url = a.get('href')
        a_title = a.text
        # print(a_url+a_title)
        urls.append({a_title: a_url})
    with open('urls.yaml', 'w', encoding='utf-8') as file:
        yaml.safe_dump(urls, file)
    return urls


def read_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


#
def if_has_next(url_next):
    html = get_html_text(url_next)
    # print(html)
    # with open('urls.html', 'w', encoding='utf-8') as file:
    #     file.write(html)

    pattern = r'url_next:\s*"(.*?)"'
    match = re.search(pattern, html)
    if match:
        url_next_value = match.group(1)
        if '_' in url_next_value:
            return url_next_value
        else:
            return None
    else:
        return None


def save_page_content(url):
    html = get_html_text(url)

    html_content = html
    h = html2text.HTML2Text()
    markdown_content = h.handle(html_content)
    # print(markdown_content)
    with open('markdown_content.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)




if __name__ == '__main__':
    # 不带cookie的话，只会返回部分子链接
    # 获取URLS列表
    urls = []
    # url = 'https://www.qianbiwenxue.com/noval/41497273.html'
    # urls = fetch_and_save_urls(url)


    # if not urls:
    #     # 调用函数读取 YAML 文件
    #     urls = read_yaml_file('urls.yaml')
    # print(urls)

    # 测试有无下一页
    url = 'https://www.qianbiwenxue.com/kan/41497273/77062856.html'
    # while url:
    #     url = if_has_next(url)
    #     print(url)

    save_page_content(url)




