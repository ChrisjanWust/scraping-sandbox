#%%
from scrapy import Selector
import re
from string import whitespace

class Page:

    def __init__(self, response):
        self.body = response
        self.url = response.url


    @staticmethod
    def enforce_return(func):
        def decorated(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            if not res:
                raise RuntimeError(f'{func.__name__} failed to return a value on {self.url}, args: {args}, kwargs: {kwargs}')
            return res
        return decorated


    def clean_html_string(self, text, group_multi_space=True):
        text = self.strip(text)
        text = text.replace('\n', '')
        text = text.replace('\t', ' ')
        text = text.replace('\xa0', ' ')
        if group_multi_space:
            text = re.sub(r' {2,}', ' ', text)
        text = self.strip(text)
        return text


    @staticmethod
    def strip(text):
        remove_chars = whitespace + ':' + '\xa0' + '-' + '/' # todo: is there cases where the '-', '/' or ':' is required?
        return text.strip(remove_chars)


    def strip_join(self, texts):
        texts = [self.strip(text) for text in texts]
        return " ".join(texts)


    def strip_limit_join(self, texts, limit=200):
        full_text = ''
        for text in texts:
            text = self.strip(text)
            if len(full_text + text) > limit:
                break
            full_text += ' ' + text
        return full_text


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
            key = self.clean_html_string(self.strip_join(key_texts))
            if key:
                value_texts = tr.xpath(value_xpath).getall()
                value = self.clean_html_string(self.strip_join(value_texts))
                if value:
                    table_dict[key] = value
        return table_dict


    @staticmethod
    def remove_empty_strings(texts):
        return [text for text in texts if text]


    def extract_texts_to_dict(self, texts, separators:list=None):
        """
        :param texts: List of potential spec texts such as "Screen size: 46 inch"
        :param separators: List of string separators that should be attempted. Defaults to [': ']
        :return: dictionary of specs
        """
        texts = self.remove_empty_strings(texts)
        texts = [self.clean_html_string(text, group_multi_space=False) for text in texts]
        separators = separators or [': ', '              ']  # default value defined here to avoid a mutable default value
        specs = {}
        # determine the best separator
        best_separator = None
        best_separator_nr_splits = 0
        for separator in separators:
            nr_splits = len([True for text in texts if separator in text])
            if nr_splits > best_separator_nr_splits:
                best_separator = separator
                best_separator_nr_splits = nr_splits
        # do actual split now that best separator has been determined
        if best_separator:
            for text in texts:
                if best_separator in text:
                    key, value = [self.strip(t) for t in text.split(best_separator, 1)]
                    if key:
                        specs[key] = value
            return specs






