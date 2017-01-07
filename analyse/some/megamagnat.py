import scrapy

from base import BrandsSpider


class Spider(BrandsSpider):
    def parse(self, response):
        brands_names = []

        for item in response.css('.universal_item'): 
            brands_names.append(item.css('.title a ::text').extract_first().replace('"', '')) 

            descr_href = item.css('.link a ::attr(href)').extract_first()

            if descr_href: 
                yield scrapy.Request(descr_href, self.parse_description)

        self.add_brands(brands_names)

    def parse_description(self, response): 
        about      = response.css('.form_show h1 + p *::text').extract()
        brand_name = response.css('.form_show span.value:first-child ::text').extract_first()

        self.add_about_brand(brand_name, about)


class Food(Spider):
    name = 'megamagnat_food'
    category = 'food'
    start_urls = [
        'http://www.megamagnat.ru/tm/produkty_pitaniya/',
        'http://www.megamagnat.ru/tm/bezalkogolnye_napitki/'
    ]

class Alchogol(Spider):
    name = 'megamagnat_alchogol'
    category = 'alchogol'
    start_urls = [
        'http://www.megamagnat.ru/tm/alkogolnye_napitki/'
    ]

class Tabaco(Spider):
    name = 'megamagnat_tabaco'
    category = 'tabaco'
    start_urls = [
        'http://www.megamagnat.ru/tm/tabachnye_izdeliya/'
    ]

class Wearing(Spider): 
    name = 'megamagnat_wearing'
    category = 'wearing'
    start_urls = [
        'http://www.megamagnat.ru/tm/odejda/'
    ]

class Shoes(Spider): 
    name = 'megamagnat_shoes'
    category = 'shoes'
    start_urls = [
        'http://www.megamagnat.ru/tm/obuv/'
    ]

class ForChildren(Spider): 
    name = 'megamagnat_for_children'
    category = 'for_children'
    start_urls = [
        'http://www.megamagnat.ru/tm/tovary_dlya_detey/'
    ]

class Pets(Spider): 
    name = 'megamagnat_for_pets'
    category = 'for_pets'
    start_urls = [
        'http://www.megamagnat.ru/tm/tovary_dlya_jivotnyh/'
    ]

class Building(Spider): 
    name = 'megamagnat_building'
    category = 'building'
    start_urls = [
        'http://www.megamagnat.ru/tm/stroitelnye_tovary/'
    ]

class Sports(Spider): 
    name = 'megamagnat_sports'
    category = 'sports'
    start_urls = [
        'http://www.megamagnat.ru/tm/sportivnye_tovary/'
    ]

class Electronics(Spider): 
    name = 'megamagnat_electronics'
    category = 'electronics'
    start_urls = [
        'http://www.megamagnat.ru/tm/bytovaya_tehnika/',
        'http://www.megamagnat.ru/tm/kompyutery_i_komplektuyuschie/',
        'http://www.megamagnat.ru/tm/telefony/'
    ]

class HouseholdGoods(Spider): 
    name = 'megamagnat_household_goods'
    category = 'household_goods'
    start_urls = [
        'http://www.megamagnat.ru/tm/hozyaystvennye_tovary/'
    ]

class Beauty(Spider): 
    name = 'megamagnat_beauty'
    category = 'beauty'
    start_urls = [
        'http://www.megamagnat.ru/tm/kosmetika_i_parfyumeriya/'
    ]