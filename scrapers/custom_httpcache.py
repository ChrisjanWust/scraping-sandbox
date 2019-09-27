from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware
from scrapy.selector import Selector
from .policy import response_is_ban

class CustomHttpCacheMiddleware(HttpCacheMiddleware):

    def process_response(self, request, response, spider):
        if response_is_ban(response):
            return response
        else:
            return super().process_response(request, response, spider)

    def process_request(self, request, spider):
        if request.meta.get('dont_use_cache'):
            return
        else:
            return super().process_request(request, spider)