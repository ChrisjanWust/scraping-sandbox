from time import sleep
import logging
from scrapy import Request

class BanHandler:

    BAN_COUNT_BEFORE_SLEEP = 10
    SLEEP_SECONDS = 60 * 3
    ban_count = 0
    logger = logging.getLogger('BanHandler')
    logger.setLevel(10)


    def __init__(self, crawler_engine=None):
        pass
        # self.crawler_engine = crawler_engine


    def handle_ban(self, crawler_engine):
        self.ban_count += 1
        if self.ban_count > self.BAN_COUNT_BEFORE_SLEEP:
            self.sleep_crawler(crawler_engine)
            self.ban_count = 0


    def sleep_crawler(self, crawler_engine):
        logging.info(f"Sleeping for {self.SLEEP_SECONDS} seconds")
        crawler_engine.pause()
        sleep(self.SLEEP_SECONDS)
        crawler_engine.unpause()