# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import os

class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        item['_id'] = item['_id'][0]
        item['link'] = item['link'][0]
        item['title'] = item['title'][0]
        item['price'] = item['price'][0]
        item['characteristics'] = {
            item['names_char'][i]: item['characteristic'][i] for i in range(len(item['terms']))
        }
        del item['terms'], item['definitions']

        collection = self.mongo_base[spider.name]
        collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        return item


class LroyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        filename = os.path.basename(request.url)
        filedir = os.path.basename(item['link'][:-1])
        return f'full/{filedir}/{filename}'
