import scrapy

class JobCrawlItem(scrapy.Item):
    title = scrapy.Field()             # 职位名称
    external_path = scrapy.Field()     # 职位路径
    locations_text = scrapy.Field()    # 地点
    posted_on = scrapy.Field()         # 发布时间
    job_id = scrapy.Field()            # 职位ID
    job_url = scrapy.Field()           # 职位链接