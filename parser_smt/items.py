# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserBookItem(scrapy.Item):
    _id = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    salary = scrapy.Field()
    new_salary = scrapy.Field()
    rate = scrapy.Field()