from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['lenta']
lenta = db.lenta

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36 '
    }

url = 'https://lenta.ru'
response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

news = dom.xpath("//section[contains(@class, 'top')]//a/time/..")
for new in news:
    list_new = {}
    name = new.xpath(".//time[@class='g-time']/../text()")[0]
    names = [s.replace('\xa0', ' ') for s in name]
    data = new.xpath(".//time[@class='g-time']/@title")[0]
    link = new.xpath(".//time[@class='g-time']/../@href")
    pprint
    if link[0].find('https://'):
        link = (url + link[0])
    else:
        link = link

    list_new['name'] = name
    list_new['link'] = link
    list_new['datatime'] = data
    list_new['sours'] = url

    lenta.insert_one(list_new)



