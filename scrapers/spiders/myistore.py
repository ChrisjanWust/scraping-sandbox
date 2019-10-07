# -*- coding: utf-8 -*-
import scrapy
from .helpers import file_handler
from .helpers.html_parsers import myistore
from .helpers.CustomSpider import CustomSpider


class MyIstoreSpider(CustomSpider):

    name = 'myistore'
    start_url = 'https://www.myistore.co.za/'
    category_paths = ["mac","ipad","watch","discover-iphone"]
    categories = ["mac", "ipad", "watch", "iphone"]    

    custom_settings = {
        'FEED_URI': file_handler.allocate_output_path(spider_name=name),
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }


    def start_requests(self):
        
        for i, category_path in enumerate(self.category_paths):
            request = scrapy.Request(url=self.start_url+category_path+"/view-all", callback=self.get_each_page)
            request.cb_kwargs['category'] = self.categories[i]
            yield request

    def get_each_page(self, response, category):
        
        page_urls = response.xpath('//ol[contains(@class, "pagination")]/li/a/@href').extract()

        page_urls.append(response.request.url+"?p=1")

        for page_url in page_urls:
            request = scrapy.Request(url=page_url, callback=self.parse_listings_page)
            request.cb_kwargs['category'] = category
            yield request

    def parse_listings_page(self, response, category):
        
        parser = myistore.ListingsPage(response)

        item_urls = parser.get_item_urls()

        for item_url in item_urls:
            request = scrapy.Request(url=item_url, callback=self.parse_item_page)
            request.cb_kwargs['category'] = category
            yield request
    
    def parse_item_page(self,response, category):

        parser = myistore.ItemPage(response)
        brand, item_name = parser.get_brand_and_name()
        specs = parser.get_specs()
        image_url = parser.get_image_url()

        pricing_data = {
            "supplier":"Myistore",
            "sku": parser.get_sku(),
            "price": parser.get_price()
        }

        yield({"brand":brand, "item_name":item_name, "category":category, "price":pricing_data, "image_url":image_url, "specs":specs})