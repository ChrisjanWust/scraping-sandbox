# -*- coding: utf-8 -*-
import scrapy
from .helpers import file_handler
from .helpers.html_parsers import myistore
from .helpers.CustomSpider import CustomSpider


class MyIstoreSpider(CustomSpider):

    name = 'myistore'
    start_url = 'https://www.myistore.co.za/'
    categories = ["Mac", "iPad", "Watch", "iPhone"]

    custom_settings = {
        'FEED_URI': file_handler.allocate_output_path(spider_name=name),
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }


    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_main_page)


    def parse_main_page(self, response):
        parser = myistore.MainPage(response)
        for category in self.categories:
            url = parser.get_category_url(category)
            yield scrapy.Request(
                url=url,
                callback=self.parse_listings_page,
                cb_kwargs={'category': category},
            )


    """
    def get_each_page(self, response, category):
        
        page_urls = response.xpath('//ol[contains(@class, "pagination")]/li/a/@href').extract()

        page_urls.append(response.request.url+"?p=1")

        for page_url in page_urls:
            request = scrapy.Request(url=page_url, callback=self.parse_listings_page)
            request.cb_kwargs['category'] = category
            yield request
    """


    def parse_listings_page(self, response, category):
        parser = myistore.ListingsPage(response)

        for item_url in parser.get_item_urls():
            request = scrapy.Request(url=item_url, callback=self.parse_item_page)
            request.cb_kwargs['category'] = category
            yield request

        for page_url in parser.get_page_urls():
            request = scrapy.Request(url=page_url, callback=self.parse_listings_page)
            request.cb_kwargs['category'] = category
            yield request

    
    def parse_item_page(self, response, category):
        parser = myistore.ItemPage(response)

        pricing_data = {
            "supplier": "Myistore",
            "sku": parser.get_sku(),
            "price": parser.get_price()
        }

        yield {
            "brand": 'Apple',
            "item_name": parser.get_name(),
            "category": category,
            "price": pricing_data,
            "image_url": parser.get_image_url(),
            "specs": parser.get_specs_2()
        }

