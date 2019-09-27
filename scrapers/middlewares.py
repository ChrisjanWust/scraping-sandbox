# -*- coding: utf-8 -*-

# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
from scrapy.selector import Selector
import re

class AmazonBanDetection(object):

    def process_response(self, request, response, spider):
        selector = Selector(text=response.body)
        if b"the characters you see" in response.body \
                or selector.xpath('//*[contains(text(),"Enter the characters you see below") or contains(text(),"Type the characters you see in this image")]'):
            logging.error("We've been caught / detected as a robot - AmazonLaptopsSpiderMiddleware.process_response in middlewares.py")
            spider.wait_through_ban()
            return request
        return response


class AmazonUrlCleaner(object):


    def process_request(self, request, spider):
        """
        Remove URL parameters to avoid detection.
        If pattern not matched, simply return original URL.
        Works on relative URLs as well.
        """
        new_url_matches = re.findall(r'^.+\/dp\/[A-Z][A-Z0-9]+', request.url)
        if new_url_matches:
            logging.info(f'Changing url from {request.url} to {new_url_matches[0]}')
            request = request.replace(url=new_url_matches[0])
            return request
        return None
