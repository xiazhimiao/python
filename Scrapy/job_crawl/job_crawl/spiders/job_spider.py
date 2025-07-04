import scrapy
import json
from job_crawl.items import JobCrawlItem
import time
import random


class JobSpider(scrapy.Spider):
    name = "job_spider"
    allowed_domains = ["pultegroup.wd1.myworkdayjobs.com"]
    base_api_url = "https://pultegroup.wd1.myworkdayjobs.com/wday/cxs/pultegroup/PGI/jobs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 第一页负载（获取total）
    first_page_payload = {
        "appliedFacets": {},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    # 后续页面负载（动态更新offset）
    page_payload = {
        "appliedFacets": {},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    total_records = 0  # 总记录数

    def start_requests(self):
        """先请求第一页获取total"""
        yield scrapy.Request(
            url=self.base_api_url,
            method='POST',
            headers=self.headers,
            body=json.dumps(self.first_page_payload),
            callback=self.parse_first_page
        )

    def parse_first_page(self, response):
        """解析第一页，获取total并启动后续请求"""
        try:
            data = json.loads(response.text)
            self.total_records = data.get('total', 151)  # 默认为151
            self.logger.info(f"第一页获取到总记录数: {self.total_records}")

            # 提取第一页数据
            for job in data.get('jobPostings', []):
                yield self.parse_job(job)

            # 计算总页数并启动后续请求
            total_pages = (self.total_records + 19) // 20  # 向上取整
            for page in range(1, total_pages):
                self.page_payload['offset'] = page * 20
                time.sleep(random.uniform(1, 2))  # 每页间隔1-2秒
                yield scrapy.Request(
                    url=self.base_api_url,
                    method='POST',
                    headers=self.headers,
                    body=json.dumps(self.page_payload),
                    callback=self.parse_subsequent_pages
                )

        except Exception as e:
            self.logger.error(f"第一页解析错误: {str(e)}")
            self.total_records = 151  # 强制设置为151

    def parse_subsequent_pages(self, response):
        """解析后续页面（忽略total，直接提取数据）"""
        try:
            data = json.loads(response.text)
            for job in data.get('jobPostings', []):
                yield self.parse_job(job)

        except Exception as e:
            self.logger.error(f"后续页面解析错误: {str(e)}")

    def parse_job(self, job):
        """解析单个职位数据"""
        item = JobCrawlItem()
        item['title'] = job.get('title', 'N/A')
        item['external_path'] = job.get('externalPath', 'N/A')
        item['locations_text'] = job.get('locationsText', 'N/A')
        item['posted_on'] = job.get('postedOn', 'N/A')
        item['job_id'] = job.get('bulletFields', ['N/A'])[0]
        item['job_url'] = f"https://pultegroup.wd1.myworkdayjobs.com/en-US/PGI{job.get('externalPath', 'N/A')}"
        return item