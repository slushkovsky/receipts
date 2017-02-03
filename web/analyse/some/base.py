import json
import os

import scrapy


BRANDS_FILE = 'brands.json'
ABOUT_BRAND_FILE = 'about.json'

class BrandsSpider(scrapy.Spider): 
    category = 'unknown'

    @classmethod
    def add_brands(cls, new_brands): 
        assert isinstance(new_brands, list)

        if os.path.exists(BRANDS_FILE):
            with open(BRANDS_FILE, 'r') as f: 
                brands = json.load(f)
        else:
            brands = {}

        if not cls.category in brands: 
            brands[cls.category] = []

        brands[cls.category] = list(set(brands[cls.category] + new_brands))

        with open(BRANDS_FILE, 'w') as f: 
            json.dump(brands, f)

    @classmethod
    def add_about_brand(cls, brand_name, about): 
        assert isinstance(brand_name, str)
        assert isinstance(about, list)

        if os.path.exists(ABOUT_BRAND_FILE):
            with open(ABOUT_BRAND_FILE, 'r') as f: 
                brands_about = json.load(f)
        else:
            brands_about = {}

        brands_about[brand_name] = about

        with open(ABOUT_BRAND_FILE, 'w') as f: 
            json.dump(brands_about, f)