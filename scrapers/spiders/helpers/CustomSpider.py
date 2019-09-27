from scrapy import Spider
from . import file_handler
import logging
from scrapy.utils.log import configure_logging
from datetime import datetime

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename=f'scrapers/logs/{datetime.strftime(datetime.now(), "%Y-%m-%d %Hh%Mm%Ss")}.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class CustomSpider(Spider):

    testing_url = None

    def __init__(self, testing_url=None, **kwargs):
        self.testing_url=testing_url
        super().__init__(**kwargs)

    def closed(self, reason):
        if reason == 'finished':
            file_handler.overwrite_main_file(spider_name=self.name, current_output_file=self.settings['FEED_URI'])








