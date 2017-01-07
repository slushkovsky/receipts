import scrapy

from base import BrandsSpider


class FoodcostSpider(BrandsSpider):
    def parse(self, response):
        self.add_brands(response.css('.catalog-item-info .catalog-item-title a ::text').extract())

        next_page = response.css('#navigation_1_next_page ::attr(href)').extract_first()
        
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

class Food(FoodcostSpider):
    name = 'foodcost_food'
    category = 'food'
    start_urls = ['http://foodcost.ru/services/resources/proizvoditeli/trademarks/produkty_pitaniya/']

class Alchogol(FoodcostSpider):
    name = 'foodcost_alchogol'
    category = 'alchogol'
    start_urls = ['http://foodcost.ru/services/resources/proizvoditeli/trademarks/alkogolnye_napitki/']