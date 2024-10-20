import os

import html2text
import requests
from bs4 import BeautifulSoup


def get_html_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding  # 将响应对象的编码设置为通过分析响应内容推断出的编码,较为准确
        return r.text
    except:
        return ""


def get_url_list():
    html = get_html_text('http://www.xinhuanet.com/')

    soup = BeautifulSoup(html, 'html.parser')
    div_tag = soup.find(id="focusListNews")
    a_tags = div_tag.find_all('a')
    title_url_list = {}
    for a in a_tags:
        a_url = a.get('href')
        title_url_list[a.text.strip()] = a_url
    return title_url_list


def save_content_as_md(url, title):
    if not os.path.exists('focusListNews'):
        os.mkdir('focusListNews')
    html = get_html_text(url)
    soup = BeautifulSoup(html, 'html.parser')
    span_tags = soup.find(id="detailContent")

    h = html2text.HTML2Text()
    md = h.handle(str(span_tags))
    with open('focusListNews/' + title + '.md', 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"{title}下载完成！")


if __name__ == '__main__':
    title_url_list = get_url_list()
    for title, url in title_url_list.items():
        save_content_as_md(url, title)
