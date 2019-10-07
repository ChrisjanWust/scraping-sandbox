import re
from .page import Page
import logging


class HiddenContentException(Exception):
    pass



class ListingsPage(Page):

    def get_item_urls(self):
        return self.body.xpath('//ol[contains(@id, "products-grid")]/li[contains(@class, "item")]/a/@href').extract()

class ItemPage(Page):

    def get_brand_and_name(self):
        item_name = self.body.xpath('//div[contains(@class, "product-name")]/h1//text()')[0].extract()
        brand = 'Apple'
        return brand, item_name

    def get_image_url(self):
        return self.body.xpath('//*[@id="main-image-default"]/img/@src').get()

    def get_sku(self):
        return self.body.xpath('//p[contains(@class, "product-sku")]/text()').get()

    def get_price(self):
        return self.body.xpath('//*[contains(@id, "product-price")]/span/text()').get()

    def get_specs(self):
        
        spec_label = self.body.xpath('//table[contains(@id, "product-attribute-specs-table")]/tbody/tr/td')
        specs = []
        specs_dict = {}

        for row in spec_label:
            specs.append(row)

        for i in range(0,len(specs)-1,2):
            p_elements = specs[i+1].xpath("p")

            if len(p_elements)<1:
                specs_dict[specs[i].xpath("*/text()").get()] = specs[i+1].xpath("text()").get()
            else:
                p_array = []
                for p_element in p_elements:
                    text = p_element.xpath('text()').get()
                    if text!=None:
                        p_array.append(text)
                specs_dict[specs[i].xpath("*/text()").get()] = p_array

        return specs_dict

