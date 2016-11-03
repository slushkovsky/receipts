from base import BrandsSpider


class TruebrandsSpider(BrandsSpider): 
    def parse(self, response): 
        self.add_brands(response.css('#brands-list li a ::text').extract())


class Food(TruebrandsSpider): 
    category = 'food'
    start_urls = ['http://truebrands.ru/cat/grocery/']