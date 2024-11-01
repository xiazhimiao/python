# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PeopleNewsCrawlerPipeline:
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

        self.logger.info("Database connection info: db=%s, host=%s, user=%s, password=%s", self.db, self.host,
                          self.user, self.password)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            self.logger.error("Failed to open database connection. Error: %s", e)
            raise

    def close_spider(self, spider):
        try:
            self.connection.close()
        except Exception as e:
            self.logger.error("Failed to close database connection. Error: %s", e)

    def process_item(self, item, spider):
        # self.logger.debug("111111111111111111111111111")
        try:
            sql = "INSERT INTO people_news (href, title,time,source,author,content) VALUES (%s, %s,%s, %s,%s, %s)"
            self.cursor.execute(sql, (
            item['href'], item['title'], item['time'], item['source'], item['author'], item['content']))
            self.connection.commit()
        except pymysql.err.ProgrammingError as e:
            self.logger.error("ProgrammingError when inserting data. SQL: %s, Data: (%s, %s). Error: %s",
                              sql, item['href'], item['title'], e)
            raise DropItem("Failed to insert item due to ProgrammingError")
        except pymysql.err.IntegrityError as e:
            self.logger.error("IntegrityError when inserting data. SQL: %s, Data: (%s, %s). Error: %s",
                              sql, item['href'], item['title'], e)
            raise DropItem("Failed to insert item due to IntegrityError")
        except Exception as e:
            self.logger.error("Unexpected error when inserting data. SQL: %s, Data: (%s, %s). Error: %s",
                              sql, item['href'], item['title'], e)
            raise DropItem("Failed to insert item due to unexpected error")
        return item
