import re
from .page import Page
import logging


class HiddenContentException(Exception):
    pass


class MainPage(Page):

    def get_subcategory_urls(self, category_path):
        xpath = f'//div[contains(@class, "sub-nav") and contains(div[contains(@class, "title")]/text(),"{category_path[0]}")]//span[contains(@class, "sub-nav")]/li/a'
        if category_path[1]:
            # if the subcategory name is specified, only select links which match that text
            xpath += f'[normalize-space()="{category_path[1]}"]'
        xpath += '/@href'

        return self.body.xpath(xpath).getall()

    def get_subsubcategory_urls(self, category_path):
        xpath = f'//div[contains(@class, "sub-nav") and normalize-space(div[contains(@class,"title")])="{category_path[0]}"]' \
            f'//span[contains(@class, "sub-nav")]'
        if category_path[1]:
            xpath += f'[normalize-space(li/a)="{category_path[1]}"]'
        xpath += '//ul/li/a'
        if category_path[2]:
            xpath += f'[normalize-space()="{category_path[2]}"]'

        see_all_xpath = xpath + '[contains(text(),"See all")]'
        if self.body.xpath(see_all_xpath).getall():
            logging.warning(f"Some subsubcategories hidden for this xpath {xpath}")

        xpath_urls = xpath + '/@href'
        return self.body.xpath(xpath_urls).getall()



class SubcategoryPage(Page):

    def get_subsubcategory_url(self, subsubcategory):
        return self.body.xpath(f'//div[contains(@class, "mak-category__feature-list")]//a[normalize-space()="{subsubcategory}"]/@href').get()

    def get_all_subsubcategory_urls(self):
        return self.body.xpath('//div[contains(@class, "mak-category__feature-list")]//a/@href').getall()


class ListingsPage(Page):

    def get_item_urls(self):
        return self.body.xpath('//div[contains(@class,"productListContainer")]//div[contains(@class,"product-tile-inner")]//a[1]/@href').getall()

    def get_next_page_url(self):
        return self.body.xpath('//div[contains(@class,"pagination")]//li[contains(@class,"next")]//a/@href').get()


class ItemPage(Page):

    def get_itemprop(self, property_name):
        return self.body.xpath(f'//span[@itemprop="{property_name}"]/text()').get()

    def get_title(self):
        texts = self.body.xpath('//div[contains(@class,"product-details")]/span[contains(@class,"name")]/b[contains(@class,"h1")]//text()').getall()
        return self._strip_and_join(texts)

    def get_brand_and_name(self):
        brand = self.get_itemprop('brand')
        title = self.get_title()
        if title.startswith(brand):
            title = title.replace(brand, 1)
        return brand, title

    def get_image(self):
        return self.body.xpath('//div[contains(@class,"gallery")]//img/@src').get()

    def get_category_path(self):
        return self.body.xpath('//ol[contains(@class,"breadcrumb")]/li/a/text()').getall()

    def get_specs(self):
        # for some reason, there are are 2 formats that specs are displayed in (even in one model)
        # format 1: regular table
        specs_1 = self._extract_table_to_dictionary(
            row_xpath='//tr[contains(td/@class,"attr")]',
            key_xpath='.//td[contains(@class,"attr")]//text()',
            value_xpath='.//td[2]//text()'
        )
        # format 2: wanna-be-table columns
        specs_2 = self._extract_table_to_dictionary(
            row_xpath='//div[contains(@class,"content") and @class="content" and contains(div/a/text(),"Details")]//div[contains(@class,"12") and contains(div/@class,"4")]',
            key_xpath='.//div[1]//text()',
            value_xpath='.//div[2]//text()'
        )
        return {**specs_1, **specs_2}

