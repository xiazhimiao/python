import codecs
import concurrent
import os
import sys
import threading
import time
import unittest
import re
import requests
import yaml
from bs4 import BeautifulSoup
import html2text
import concurrent.futures


# 获取网页源码
def get_html_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'cookie': 'zh_choose=n; jq_Obj=1; ff54ff0fa0f557568e6e69d35b815894=73f2a200eb3045f34a6a63b30673ccc8; _ga=GA1.1.1325912085.1731486613; zh_choose=n; _ga_YN9485YEKE=GS1.1.1731486612.1.1.1731488916.0.0.0'
        ,

    }
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding  # 将响应对象的编码设置为通过分析响应内容推断出的编码,较为准确
        return r.text
    except:
        return ""


def fetch_and_save_urls(url):
    html = get_html_text(url)
    if html == "":
        sys.exit("因html为空，导致系统提前终止")
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


def save_page_content(html_content, chapter):
    # soup = BeautifulSoup(html_content, 'html.parser')
    # soup = BeautifulSoup(html_content, 'lxml')  lxml可能会更快，好像更慢了
    # chapter = soup.find('div', id='mlfy_main_text').find('h1').text
    h = html2text.HTML2Text()
    markdown_content = ((h.handle(html_content)
                         .replace('_', '')
                         .replace(' ', ''))
                        .replace('铅笔小说网qianbiwenxue.com', ''))
    # print(markdown_content)
    with open('她的秘密/' + chapter + '.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)


def replace_content(css_dict, html_content):
    icon_dict = {}
    for icon_class, content in css_dict:
        try:
            # print(icon_class)
            # print(content)
            # utf8_content = codecs.decode(content.encode('utf-16be'), 'utf-8')

            # encoded_str = r'\5929'
            content_bytes = bytes([int(content[1:3], 16), int(content[3:], 16)])
            decoded_str = content_bytes.decode('utf-16be')
            # print(decoded_str)

            icon_dict[f'icon-{icon_class}'] = decoded_str

        except UnicodeDecodeError:
            print(f"无法正确解码 icon-{icon_class} 的内容。")

    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find('div', id='mlfy_main_text')
    for icon_class, utf8_content in icon_dict.items():
        for i_tag in div.find_all('i', {'class': lambda c: icon_class in c}):
            # 如果原来的<i>标签没有内容，直接插入转码后的内容
            if not i_tag.string:
                i_tag.string = utf8_content
            else:
                # 如果原来有内容，在原有内容基础上添加转码后的内容
                i_tag.string = i_tag.string + utf8_content

    return str(soup)


def read_css_dict(css_url):
    try:
        with open('css_dict.yml', 'r') as file:
            css_dict = yaml.safe_load(file)
            print('读取本地:css_dict')
            return css_dict
    except FileNotFoundError:
        css_content = get_html_text(css_url)
        if css_content == '':
            sys.exit("因css错误导致提前退出")
        icon_pattern = r'\.icon-(.*?):before\s*\{\s*content:\s*"(.*?)";\s*\}'
        css_dict = re.findall(icon_pattern, css_content)
        with open('css_dict.yml', 'w') as file:
            yaml.safe_dump(css_dict, file)
        return css_dict


def read_urls(url):
    try:
        with open('urls.yaml', 'r') as file:
            print('读取本地:urls')
            return yaml.safe_load(file)
    except FileNotFoundError:
        return fetch_and_save_urls(url)


def process_html_pages(chapter, url):
    # 获取线程id
    thread_id = threading.current_thread().ident
    # html = 'https://www.qianbiwenxue.com/kan/41497273/77062856.html'
    html_content = ''
    # 测试有无下一页
    while url:
        html = get_html_text(url)
        # 插入文字
        html_content += replace_content(css_dict, html)
        url = if_has_next(url)

    # 转换为md
    save_page_content(html_content, chapter)

    # 计时器
    end_time = time.time()
    elapsed_time = end_time - start_time
    return f'线程：{thread_id}下载章节《{chapter}》完毕--当前用时：{elapsed_time:.5f} 秒。'


if __name__ == '__main__':
    if not os.path.exists('她的秘密'):
        os.mkdir('她的秘密')
    # 不带cookie的话，只会返回部分子链接
    # 获取URLS列表
    url = 'https://www.qianbiwenxue.com/noval/41479393.html'
    # url = 'https://www.invalid_url.com'

    # 经分析，替换字符采用UTF-16BE（Big Endian，大端序）
    # https://www.qianbiwenxue.com/static/css/fonts.css?v=c560a99cd812e57bb8e2e8fdde5f1650（唯一）
    css_url = 'https://www.qianbiwenxue.com/static/css/fonts.css?v=c560a99cd812e57bb8e2e8fdde5f1650'
    # css_url = 'https://www.invalid_css_url.com'

    # 加载url列表
    url_s = read_urls(url)
    # 加载插入文字
    css_dict = read_css_dict(css_url)
    start_time = time.time()
    # 失败列表
    failed_tasks = []
    # 开启线程池提交任务
    print('开启线程池提交任务')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_task = {executor.submit(process_html_pages, list(item.keys())[0], list(item.values())[0]): item for
                          item in url_s}
        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            task_chapter = list(task.keys())[0]
            task_url = list(task.values())[0]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"{task_chapter} 产生了一个异常：{exc}")
                failed_tasks.append(task)

    # 手动失败列表
    manual_failed_tasks_list = []
    if failed_tasks:
        print("失败列表不为空，开始执行失败列表")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_task = {executor.submit(process_html_pages, list(item.keys())[0], list(item.values())[0]): item
                              for item in failed_tasks}
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                task_chapter = list(task.keys())[0]
                task_url = list(task.values())[0]
                try:
                    result = future.result()
                    print(result)
                except Exception as exc:
                    print(f"任务《{task_chapter}》再次失败，手动获取 ")
                    manual_failed_tasks_list.append(task_chapter)
    if manual_failed_tasks_list:
        print('打印失败章节')
        print(manual_failed_tasks_list)
    else:
        print('全部成功！！！')



