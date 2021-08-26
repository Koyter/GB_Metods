import scrapy
from scrapy.http import HtmlResponse
from parser_smt.items import ParserBookItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/Python/?stype=0']
    url = 'https://www.labirint.ru'

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            long_next_page = self.start_urls[0][:-8] + next_page
            yield response.follow(long_next_page, callback=self.parse)

        links = [f'https://www.labirint.ru{url.extract()}' for url in response.xpath("//a[@class='cover']/@href")]
        for link in links:
            yield response.follow(link, callback=self.book_parser)

    def book_parser(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//div[@class='authors']/a/text()").extract_first()
        salary = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        new_salary = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        yield ParserBookItem(link=link, name=name, author=author, salary=salary, new_salary=new_salary, rate=rate)
