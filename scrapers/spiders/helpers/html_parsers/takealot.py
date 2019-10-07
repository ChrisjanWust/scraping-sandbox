import re
from .page import Page




class MainPage(Page):

    @Page.enforce_return
    def get_department_url(self, category_path):
        xpath = f'//li[contains(@class,"menuitem") and contains(a[contains(@class,"baselink")]/span/text(),"{category_path[0]}")]' \
            f'//div/ul/li/a[contains(span/text(),"{category_path[1]}")]/@href'
        return self.body.xpath(xpath).get()




class DepartmentPage(Page):

    @Page.enforce_return
    def get_category_url(self, category):
        return self.body.xpath(f'//div[contains(h3/text(),"Departments")]/ul/li[contains(@class,"expanded-cat")]/a[normalize-space()="{category}"]/@href').get()




class CategoryPage(Page):

    @Page.enforce_return
    def get_subcategory_url(self, subcategory):
        return self.body.xpath(f'//div[contains(h3/text(),"Departments")]/ul/li[contains(@class,"indent")]/a[normalize-space()="{subcategory}"]/@href').get()




class ListingsPage(Page):

    def get_item_urls(self):
        return self.body.xpath('//div[contains(@class,"product-listings")]//li[contains(@class,"result-item")]/div/p/a/@href').getall()


    @Page.enforce_return
    def get_all_listings_urls(self):
        # first try "filtering" according to the department (if there is only one)
        department_links = self.body.xpath('//div[contains(h3/text(),"Departments")]/ul/li[contains(@class,"expanded-cat")]/a/@href').getall()
        if len(department_links) == 1:
            return department_links[0]
        # look for "See all" links
        see_all_links = self.body.xpath('//div[contains(@class,"content")]//a[contains(.//text(),"See all")]/@href').getall()
        if see_all_links:
            return see_all_links[0]


    def get_next_page_url(self):
        return self.body.xpath('//*[contains(@class,"pagination")]//a[contains(@class,"next")]/@href').get()




class ItemPage(Page):

    @Page.enforce_return
    def get_image(self):
        return self.body.xpath('//div[contains(@class,"gallery")]//div[contains(@class,"image-box")]/img/@src').get()


    @Page.enforce_return
    def get_title(self):
        return self.body.xpath('//div[contains(@class,"product-title")]//h1/text()').get()


    def get_subtitle(self):
        texts = self.body.xpath('//div[contains(@class,"product-title")]//span[contains(@class,"subtitle")]//text()').getall()
        return self.strip_join(texts)


    @Page.enforce_return
    def get_brand(self):
        texts = self.body.xpath('//div[contains(@class,"product-title")]//span[contains(@class,"brand-link")]//text()').getall()
        return self.strip_join(texts)


    @Page.enforce_return
    def get_price(self):
        texts = self.body.xpath('//div[contains(@class,"buybox-module_price")]/span[contains(@class,"currency")]//text()').getall()
        return self.strip_join(texts)


    @Page.enforce_return
    def get_specs(self):
        return self.extract_table_to_dict(
            row_xpath='//*[@id="product-tabs"]//div[contains(@class,"product-info")]//tr[contains(@class,"product-info")]',
            key_xpath='.//td[contains(@class,"title")]/text()',
            value_xpath='.//td[2]//text()'
        )