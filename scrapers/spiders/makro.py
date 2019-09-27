# -*- coding: utf-8 -*-
import scrapy
from .helpers import file_handler
from .helpers.html_parsers import makro
from .helpers.CustomSpider import CustomSpider


class MakroSpider(CustomSpider):

    name = 'makro'
    start_url = 'https://www.makro.co.za/'

    # list of categories to be scraped
    category_paths = [
        ['Electronics & Computers', "Televisions", "LED"],
        ['Electronics & Computers', "Cellphones", "Cellphone Handsets"],
        ['Electronics & Computers', "Cameras", "Camera Lenses"],
        ['Electronics & Computers', "Cameras", "Digital Cameras"],
        ['Electronics & Computers', "Cameras", "Video & Action Cameras"],
        ['Electronics & Computers', "Watches"],
        ['Electronics & Computers', "Computers & Tablets", "Laptops & Notebooks"],
        ['Electronics & Computers', "Computers & Tablets", "Screens"],
        ['Electronics & Computers', "Audio & Video", "Audio Components"],
        # ['Electronics & Computers', "Audio & Video", "Home Theatre Systems"],
        # ['Electronics & Computers', "Audio & Video", "Home Audio"],
        # ['Electronics & Computers', "Audio & Video", "Sound Bars"],
        # ['Electronics & Computers', "Audio & Video", "Audio Speakers Accessories"],
        ['Games & Gaming', 'Video Games', 'Software'],
        ['Games & Gaming', 'Video Games', 'Consoles'],
        ['Appliances']
    ]

    custom_settings = {
        'FEED_URI': file_handler.allocate_output_path(spider_name=name),
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }


    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_main_page)


    def parse_main_page(self, response):
        parser = makro.MainPage(response)


        for category_path in self.category_paths:
            category_path = category_path + [''] * (3 - len(category_path))  # fill in if full category path not specified

            subsubcategory_urls = parser.get_subsubcategory_urls(category_path)  # may throw a HiddenContent exception - not caught because there is no alternative yet
            for url in subsubcategory_urls:
                url = self.change_url_to_100_per_page(url)
                yield scrapy.Request(url=response.urljoin(url),
                                     callback=self.parse_listings_page)


    def parse_subcategory_page(self, response):
        parser = makro.SubcategoryPage(response)
        subsubcategory = response.meta['subsubcategory']

        if subsubcategory:
            subsubcategory_urls = [parser.get_subsubcategory_url(subsubcategory)]
        else:  # no subsubcategory specified, select all
            subsubcategory_urls = parser.get_all_subsubcategory_urls()

        for url in subsubcategory_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_listings_page)


    def parse_listings_page(self, response):

        parser = makro.ListingsPage(response)
        item_urls = parser.get_item_urls()

        if not item_urls:
            # this isn't a listings page. Look for a link to a listings page
            # wierd issue, seems to be connected to network load. Doesn't occur when not continuing with requests (if stopped here, the spider load is much lighter)
            # todo: 1. test issue on solid internet connection at home, 2. (if issue persists) Retry problematic URLs with Splash's full browser
            manual_retries = response.meta.get('manual_retries', 0) + 1
            self.logger.warning(f"Didn't find any items on this listings_page ({response.url}) - retrying {manual_retries}")
            if manual_retries < 10:
                yield scrapy.Request(url = response.url,
                                     callback=self.parse_listings_page,
                                     dont_filter=True,
                                     meta={'manual_retries': manual_retries})
            else:
                file_handler.save_problematic_page(response)
                raise RuntimeError(f"GAVE UP - Couldn't find any items on this listing page ({response.url}) - gave up after {manual_retries} retries")
            return
        else:
            if response.meta.get('manual_retries'):
                self.logger.info(f"Actually successfully retried url {response.url}, retry nr {response.meta.get('manual_retries')}")

        for item_url in item_urls:
            yield scrapy.Request(url=response.urljoin(item_url),callback=self.parse_item_page)

        next_page_url = parser.get_next_page_url()
        if next_page_url:
            yield scrapy.Request(url=response.urljoin(next_page_url), callback=self.parse_listings_page)


    def parse_item_page(self, response):
        parser = makro.ItemPage(response)
        specs = parser.get_specs()
        specs['gtin'] = parser.get_itemprop('gtin13')
        brand, name = parser.get_brand_and_name()

        pricing_data = {
            'supplier': 'Makro',
            'sku': parser.get_itemprop('productId') or parser.get_sku(),
            'price': parser.get_itemprop('price'),
        }

        item = {
            'model_nr': parser.get_itemprop('model'),
            'brand': brand or name.split(' ', 1)[0],
            'name': name,
            'url': response.url,
            'specs': specs,
            'image_url': parser.get_image(),
            'category': parser.get_category_path(),
            'pricing_data': pricing_data
        }

        yield item


    def change_url_to_100_per_page(self, url):
        # warning: if parameters are already in the url but pageSize isn't, the function won't increase the results per page
        if '?' in url:
            self.logger.warning("Didn't attempt to change URL because parameters are already present")
            return url
        url = url.replace('#', '')  # remove `#` at the end
        url += '?pageSize=100&q=%3Arelevance'
        return url

