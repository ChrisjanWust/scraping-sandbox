# -*- coding: utf-8 -*-
import scrapy
from .helpers import file_handler
from .helpers.html_parsers import takealot
import json
from .helpers.CustomSpider import CustomSpider
from scrapy_splash import SplashRequest
import re


class TakealotSpider(CustomSpider):

    name = 'takealot'
    start_url = 'https://www.takealot.com/'

    # list of categories to be scraped
    category_paths = [
        ['Electronics & Computers', "TV's"],
        ['Electronics & Computers', 'Monitors'],
        ['Electronics & Computers', 'Laptops'],
        ['Electronics & Computers', 'Audio'],
        ['Electronics & Computers', 'Wearable Tech'],
        ['Cellphones & Tablets', 'Cellphones'],
        ['Cellphones & Tablets', 'Smartphones'],
        ['Cellphones & Tablets', 'Tablets & Kindles'],
        ['Appliances', 'Small Appliances'],
        ['Appliances', 'Large Appliances'],
        ['Appliances', 'Home Appliances'],
        ['Gaming, Movies & Music', 'Gaming', 'Consoles'],
        ['Gaming, Movies & Music', 'Gaming', 'Games'],
        ['Electronics & Computers', 'Cameras', 'Cameras & Lenses', 'Cameras']
    ]

    custom_settings = {
        'FEED_URI': file_handler.allocate_output_path(spider_name=name),
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }


    with open('scrapers/splash_settings.json') as f:
        splash_settings = json.load(f)
    custom_settings = {**custom_settings, **splash_settings}


    def start_requests(self):
        yield SplashRequest(url=self.start_url, callback=self.parse_main_page)


    def parse_main_page(self, response):
        try:
            parser = takealot.MainPage(response)

            for category_path in self.category_paths:
                category_url = parser.get_department_url(category_path)
                category_url = self.change_url_to_50_per_page(category_url)
                if len(category_path) == 2:
                    yield SplashRequest(
                        url=response.urljoin(category_url),
                        callback=self.parse_listings_page,
                        dont_filter=True
                    )
                else:
                    yield SplashRequest(
                        url=response.urljoin(category_url),
                        callback=self.parse_department_page,
                        meta={'remaining_category_path':category_path[2:]},
                        dont_filter=True
                    )
        except RuntimeError:
            file_handler.save_problematic_page(response)
            # traceback.print_last()


    def parse_department_page(self, response):
        parser = takealot.DepartmentPage(response)
        remaining_category_path = response.meta['remaining_category_path']
        category_url = parser.get_category_url(remaining_category_path[0])
        if type(category_url) is not str:
            self.logger.error(f'Returned category_url is {category_url} of type {type(category_url)}')
        del remaining_category_path[0]
        if not remaining_category_path:
            yield SplashRequest(
                url=response.urljoin(category_url),
                callback=self.parse_listings_page,
                dont_filter=True
            )
        else:
            yield SplashRequest(
                url=response.urljoin(category_url),
                callback=self.parse_category_page,
                meta={'remaining_category_path': remaining_category_path},
                dont_filter=True
            )


    def parse_category_page(self, response):
        parser = takealot.CategoryPage(response)
        remaining_category_path = response.meta['remaining_category_path']
        if len(remaining_category_path) > 1:
            raise NotImplementedError("Category paths more than 4 levels deep not supported")
        subcategory_url = parser.get_subcategory_url(remaining_category_path[0])
        yield SplashRequest(
            url=response.urljoin(subcategory_url),
            callback=self.parse_listings_page
        )


    def parse_listings_page(self, response):
        if 'promotion/apple' in response.url:
            self.logger.warn(f"Arrived at {response.url}, referrer: {response.request.headers.get('Referer')}")

        parser = takealot.ListingsPage(response)
        item_urls = parser.get_item_urls()

        if not item_urls:
            # this isn't a listings page. Look for a link to a listings page
            listings_url = parser.get_all_listings_urls()
            yield SplashRequest(url=response.urljoin(listings_url), callback=self.parse_listings_page)

        for item_url in item_urls:
            yield scrapy.Request(url=self.change_to_api_url(item_url),callback=self.parse_item_json)

        next_page_url = parser.get_next_page_url()
        if next_page_url:
            yield SplashRequest(url=response.urljoin(next_page_url), callback=self.parse_listings_page)



    def parse_item_json(self, response):
        response_text = response.body.decode('utf-8')
        item_data = json.loads(response_text)

        specs = {spec['display_name']: spec['displayable_text'] for spec in item_data['product_information']['items']}

        category = [category['name'] for category in item_data['breadcrumbs']['items']]
        image_urls = item_data['gallery']['images']
        image_url = image_urls[0] if image_urls else None
        stock_status = item_data['stock_availability']['status'] if item_data.get('stock_availability') \
            else item_data['event_data']['documents']['product']['in_stock']

        pricing_data = {
            'supplier': 'Takealot',
            'id': item_data['core']['id'],
            'rating': item_data['core']['star_rating'],
            'sku': item_data['data_layer']['sku'],
            'price': item_data['data_layer']['totalPrice'],
            'stock_status': stock_status
        }

        item = {
            'name': item_data['core']['title'],  # todo: should change to model / name / such
            'subtitle': item_data['core']['subtitle'],  # todo: should change to whatever it is (like model number)
            'brand': item_data['core']['brand'],
            'category': category,
            'url': item_data['sharing']['url'],
            'image_url': image_url,
            'specs': specs,
            'pricing_data': pricing_data
        }

        yield item


    def change_url_to_50_per_page(self, url):
        return url.replace('&rows=20&', '&rows=50&', 1)


    def change_to_api_url(self, url):
        plid = re.search('PLID\d{6,}', url)[0]
        return f'https://api.takealot.com/rest/v-1-9-0/product-details/{plid}?platform=desktop'

