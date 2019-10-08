import re
from .page import Page
import logging



class MainPage(Page):

    @Page.enforce_return
    def get_category_url(self, category_name):
        return self.body.xpath(f'//li[normalize-space(a)="{category_name}"]//a[normalize-space()="View All"]/@href').get()


class ListingsPage(Page):

    @Page.enforce_return
    def get_item_urls(self):
        return self.body.xpath('//ol[contains(@id, "products-grid")]/li[contains(@class, "item")]/a/@href').extract()

    def get_page_urls(self):
        return self.body.xpath('//ol[contains(@class, "pagination")]/li/a/@href').extract()


class ItemPage(Page):

    @Page.enforce_return
    def get_name(self):
        return self.body.xpath('//div[contains(@class, "product-name")]/h1//text()')[0].extract()

    @Page.enforce_return
    def get_image_url(self):
        return self.body.xpath('//*[@id="main-image-default"]/img/@src').get()

    @Page.enforce_return
    def get_sku(self):
        return self.body.xpath('//p[contains(@class, "product-sku")]/text()').get()

    @Page.enforce_return
    def get_price(self):
        return self.body.xpath('//*[contains(@id, "product-price")]/span/text()').get()

    @Page.enforce_return
    def get_specs(self):

        spec_label = self.body.xpath('//table[contains(@id, "product-attribute-specs-table")]/tbody/tr/td')
        specs = []
        specs_dict = {}

        for row in spec_label:
            specs.append(row)

        for i in range(0, len(specs) - 1, 2):
            p_elements = specs[i + 1].xpath("p")

            if len(p_elements) < 1:
                specs_dict[specs[i].xpath("*/text()").get()] = specs[i + 1].xpath("text()").get()
            else:
                p_array = []
                for p_element in p_elements:
                    text = p_element.xpath('text()').get()
                    if text != None:
                        p_array.append(text)
                specs_dict[specs[i].xpath("*/text()").get()] = p_array

        return specs_dict

    @Page.enforce_return
    def get_specs_2(self):
        spec_labels = self.body.xpath('//table[contains(@id, "product-attribute-specs-table")]/tbody/tr/td')
        specs = {}

        for th, td in zip(spec_labels[::2], spec_labels[1::2]):
            key = th.xpath('.//text()').get()
            values = td.xpath('.//text()').getall()
            values = [value.strip() for value in values]
            specs[key] = [value for value in values if value]

        return specs


    @Page.enforce_return
    def get_specs_3(self):
        return self.extract_table_to_dict(
            row_xpath='//table[contains(@id, "product-attribute-specs-table")]/tbody/tr/td[strong]',
            key_xpath='.//text()',
            value_xpath='../td[not(strong)]//text()',
        )



