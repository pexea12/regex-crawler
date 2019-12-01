import scrapy
import re
from datetime import datetime


class MainSpider(scrapy.Spider):
    name = 'main'

    def __init__(self, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)

        self.url_items += kwargs.get('url_items', [])
        # url_items is a list of item {url: 'http://google.com', regex: 'google'}

        self.db = kwargs.get('db')

    def start_requests(self):
        for item in self.url_items:
            yield scrapy.Request(
                url=item['url'],
                callback=self.parse,
                cb_kwargs={
                    'regex': item['regex'],
                },
            )

    def parse(self, response, **kwargs):
        text = response.xpath('string(//body)').get()

        matches = re.finditer(kwargs.get('regex'), text)

        log = {
            'time': datetime.now().isoformat(),
            'url': response.url,
            'regex': kwargs.get('regex'),
            'matches': [],
        }

        for match in matches:
            log['matches'].append([
                {
                    'text': match.group(0),
                    'start': match.start(),
                    'end': match.end(),
                },
            ])

        self.db.insert(log)

