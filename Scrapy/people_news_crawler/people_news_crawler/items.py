# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PeopleNewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    import scrapy

    """存储从人民网爬取的新闻数据项。"""

    href = scrapy.Field()
    """新闻文章的链接地址。"""
    title = scrapy.Field()
    """新闻文章的标题。"""
    # text = scrapy.Field()
    # """新闻文章对应的<a>标签中的文本内容。"""

    time = scrapy.Field()
    """新闻文章的发布时间。"""
    source = scrapy.Field()
    """新闻文章的来源。"""
    author = scrapy.Field()
    """新闻文章的作者。"""
    content = scrapy.Field()
    """新闻文章的详细内容。"""
