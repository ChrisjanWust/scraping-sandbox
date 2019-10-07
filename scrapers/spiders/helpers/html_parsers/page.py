from scrapy import Selector
import re
from string import whitespace

class Page:

    def __init__(self, selector=None, body=None):
        self.body = selector or Selector(text=body)


    @staticmethod
    def _clean_html_string(text):
        text = text.strip()
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = text.replace('\xa0', ' ')
        text = re.sub(r' {2,}', ' ', text)
        return text

    @staticmethod
    def strip(text):
        remove_chars = whitespace + ':' + '\xa0'
        texts = [text.strip(remove_chars) for text in texts]
    def strip_join(self, texts):
        return " ".join(texts)


    def extract_table_to_dict(self, row_xpath, key_xpath, value_xpath):
        """
        Note that it doesn't necessary have to be a table, just be represented in a table like structure
        :param row_xpath: xpath selecting all container elements wherein both the headers and values lie
        :param key_xpath: xpath relative to the row_xpath selecting all text that should be regarded as key text. These will be joined into a single key string.
        :param value_xpath: xpath relative to the row_xpath selecting all text that should be regarded as value text. These will be joined into a single value string.
        :return: Dictionary with key:value strings for each "row"
        """
        table_dict = {}
        containers = self.body.xpath(row_xpath)
        for tr in containers:
            key_texts = tr.xpath(key_xpath).getall()
            key = self._clean_html_string(self._strip_and_join(key_texts))
            value_texts = tr.xpath(value_xpath).getall()
            value = self._clean_html_string(self._strip_and_join(value_texts))
            table_dict[key] = value
        return table_dict

