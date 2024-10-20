import html2text
import requests

from bs4 import BeautifulSoup
import os


def get_url_list():
    # 获取python3首页文章内章节url
    url = 'https://www.runoob.com/python3/python3-tutorial.html'
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding  # 将响应对象的编码设置为通过分析响应内容推断出的编码,较为准确
    # print(resp.text)
    # with open('tutorial.html', 'wb') as f:
    #     f.write(resp.content)

    # 接下来对text使用dom处理,使用bs4
    soup = BeautifulSoup(resp.text, 'html.parser')
    div_tag = soup.find('div', class_='design')
    # 创建列表用来存储url
    url_list = []
    title = []
    a_tags = div_tag.find_all('a')
    for a in a_tags:
        url_list.append(a.get('href'))
        title.append(a.get_text().strip())
    return url_list, title


def joint(url_list_):
    # 循环列表构建url
    urls = []
    for url in url_list_:
        url0 = 'https://www.runoob.com'
        # 如果URL 不以 / 开头，添加 /
        if not url.startswith('/'):
            url = '/' + url
        # 如果URL 不以/python3开头则添加
        if not url.startswith('/python3/'):
            url = '/python3' + url
        url0 += url
        urls.append(url0)
    # for url in urls:
    #     print(url)
    return urls


def process_string(s):
    parts = s.split('/')
    return parts[-1] if parts else s


def save_page_content(html_content):
    h = html2text.HTML2Text()
    return h.handle(html_content)


def get_html(urls_, title_):
    if not os.path.exists('python3_body'):
        os.mkdir('python3_body')
    for url, title in zip(urls_, title_):
        resp = requests.get(url)
        resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, 'html.parser')
        div = soup.find('div', class_='article-intro')
        md = save_page_content(str(div))

        title = title.replace('/', '_')

        with open('python3_body/' + title + '.md', 'w', encoding='utf-8') as f:
            f.write(md)
        print(f'完成下载{title}')


if __name__ == '__main__':
    # 获取python3首页文章内章节url
    url_list = get_url_list()[0]
    title_list = get_url_list()[1]

    # 拼接url
    urls = joint(url_list)
    # print(urls)

    # 请求源码，并且下载到文件夹内
    get_html(urls, title_list)
