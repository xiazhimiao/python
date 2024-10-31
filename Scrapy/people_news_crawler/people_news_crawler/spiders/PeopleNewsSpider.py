import scrapy

from ..items import PeopleNewsCrawlerItem


class PeopleNewsSpider(scrapy.Spider):
    name = 'people_news'
    start_urls = [
        # 这里可以先放置一个网址 n，后续可以用列表推导式生成多个网址
        'http://society.people.com.cn/GB/86800/index1.html'
    ]

    start_urls = [f'http://society.people.com.cn/GB/86800/index{i}.html' for i in range(1, 18)]

    def parse(self, response):
        div = response.css('.ej_list_box.clear')
        for ul in div.css('ul'):
            a_tags = ul.css('a')
            for a_tag in a_tags:
                if 'href' in a_tag.attrib:
                    item = PeopleNewsCrawlerItem()
                    item['href'] = 'http://society.people.com.cn' + a_tag.attrib['href']
                    item['title'] = a_tag.css('::text').get()
                    yield scrapy.Request(item['href'], callback=self.parse_article, meta={'item': item})

    def parse_article(self, response):
        item = response.meta['item']
        div = response.css('.col.col-1.fl')


        # source and time
        time_div = div.css('.col-1-1.fl')
        a = time_div.css('a')
        time_text = time_div.css('::text').get()
        a_text = a.css('::text').get()
        item['source'] = a_text

        if time_text:
            time_parts = time_text.split('|')
            if time_parts:
                item['time'] = time_parts[0].strip()

        # 内容
        rm_txt_con_div = div.css('.rm_txt_con.cf')
        content = ''
        p_tags = rm_txt_con_div.css('p')
        for p in p_tags:
            p_text = p.css('::text').get()
            if p_text:
                content += p_text
        item['content'] = content

        # 责编
        edit_div = rm_txt_con_div.css('.edit.cf')
        edit_text = edit_div.css('::text').get()
        if edit_text:
            item['author'] = edit_text

        yield item
