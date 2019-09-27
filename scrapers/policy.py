from rotating_proxies.policy import BanDetectionPolicy
import logging
from scrapy.selector import Selector

class AmazonBanPolicy(BanDetectionPolicy):

    def response_is_ban(self, request, response):
        ban_default = super(AmazonBanPolicy, self).response_is_ban(request, response)
        # print(type(response))
        # print(response)
        # logging.warning(response)
        selector = Selector(text=response.body)
        ban_amazon = b"the characters you see" in response.body or selector.xpath(
            '//*[contains(text(),"Enter the characters you see below") or contains(text(),"Type the characters you see in this image")]')
        if ban_amazon:
            logging.error("We've been caught / detected as a robot. But retrying. - AmazonBanPolicy.response_is_ban from policy.py")
        return ban_default or ban_amazon


def response_is_ban(response):
    selector = Selector(text=response.body)
    xpath = '//*[contains(text(),"Enter the characters you see below") or contains(text(),"Type the characters you see in this image")]'
    if b"the characters you see" in response.body or selector.xpath(xpath):
        return True
    else:
        return False
