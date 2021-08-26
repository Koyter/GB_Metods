# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
import re


def edit_characteristic(values):
    pattern = re.compile('\\n +')
    values = re.sub(pattern, '', values)
    try:
        return float(values)
    except ValueError:
        return values

def get_price(value):
    try:
        return int(value)
    except:
        return value

class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(get_price),
                         output_processor=TakeFirst())
    photos = scrapy.Field()
    names_char = scrapy.Field(input_processor=MapCompose())
    characteristic = scrapy.Field(input_processor=MapCompose(edit_characteristic))
    characteristics = scrapy.Field()