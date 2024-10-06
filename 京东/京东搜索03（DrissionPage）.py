import urllib

from DrissionPage import ChromiumPage

from bs4 import BeautifulSoup

import csv


def get_url(start_url):
    # 打开浏览器
    dp = ChromiumPage()

    # 设置监听url
    dp.listen.start(start_url)

    # 访问网站
    dp.get(start_url)

    # 等待数据包加载
    resp = dp.listen.wait()
    # 获取响应数据
    html = resp.response.body
    return html


def extract(html):
    # 接下来对text使用dom处理,使用bs4
    soup = BeautifulSoup(html, 'html.parser')
    ul_tag = soup.find('ul', class_='gl-warp clearfix')
    # 创建列表用来存储每个商品的信息
    shop_list = []
    if ul_tag:
        li_tags = ul_tag.find_all('li')
        for li in li_tags:
            item_dict = {}
            # id
            sku_value = li.get('data-sku')
            item_dict['sku'] = sku_value
            # name
            name = li.find('div', class_='p-name p-name-type-2').find('em').text
            if name is not None:
                item_dict['name'] = name.strip()  # 去除前后换行或空格
            else:
                item_dict['name'] = None
            # 继续添加其他属性的提取逻辑
            item_dict['price'] = li.find('div', class_='p-price').find('i').text + '￥'
            try:
                item_dict['shop'] = li.find('div', class_='p-shop').find('a').text.strip()
            except AttributeError as e:
                item_dict['shop'] = None
                print(item_dict['name'] + '没有找到出处')
            item_dict['comments'] = li.find('div', class_='p-commit').find('a').text.strip() + '条评价'

            shop_list.append(item_dict)
        return shop_list
    else:
        print("指定的<ul>标签未找到。")
        return []


# print(html)
# with open('result1.html', 'w', encoding='utf-8') as f:
#     f.write(resp.response.body)


if __name__ == '__main__':

    '''
    构建url  https://search.jd.com/Search?keyword=%E8%AE%A1%E7%AE%97%E6%9C%BA

    https://search.jd.com/Search?keyword=%E8%AE%A1%E7%AE%97%E6%9C%BA&pvid=bfaf1a50a8ba42c6979d73e7b0799d8e&isList=0&page=3&s=56&click=0&log_id=1728189087141.3821
    https://search.jd.com/Search?keyword=%E8%AE%A1%E7%AE%97%E6%9C%BA&isList=0&page=1&s=56&click=0&log_id=1728189087141.3821

    可以打开https://search.jd.com/Search?keyword=%E8%AE%A1%E7%AE%97%E6%9C%BA&page=3
    监听也是这个url
    '''
    # 关键词及页数
    keyword = "计算机"
    page = 0  # 如果共100页，那么page就是200，，，，，page从0开始

    for page in range(200):
        # 构建url
        start_url = "https://search.jd.com/Search?keyword=" + urllib.parse.quote_plus(keyword) + "&page=" + str(page)
        # 获取响应
        html = get_url(start_url)

        # 提取信息
        item_list = extract(html)

        # 遍历列表并打印每个字典
        for item in item_list:
            print(item)

        # 写入csv
        # 创建文件

        with open('new_file.csv', 'a', encoding='utf-8', newline='') as f:
            # 以字典写入
            csv_writer = csv.DictWriter(f, fieldnames=[
                'sku', 'name', 'price', 'shop', 'comments',
            ])
            # 写入表头
            if page == 0:
                csv_writer.writeheader()
            # 写入数据
            for item in item_list:
                csv_writer.writerow(item)
