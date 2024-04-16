from pathlib import Path
import re
import scrapy
import json

class almadina(scrapy.Spider):
    name = "almadina"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 200,  # Increased concurrent requests
        'AUTOTHROTTLE_ENABLED': True,  # Enabled AutoThrottle extension
        'AUTOTHROTTLE_START_DELAY': .1,  # Initial delay for AutoThrottle
        'AUTOTHROTTLE_MAX_DELAY': .3,  # Maximum delay for AutoThrottle
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 200,  # Target concurrency for AutoThrottle
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 884393
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):
            url = f'https://www.al-madina.com/article/{i}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
       
        item['title'] = response.xpath('/html/body/main/div[5]/div/div[1]/div[1]/h1//text()').get()

        item['date'] = response.xpath('/html/head/meta[13]/@content').get()

        pattern = r'class=\"article-body\">(.*?)class=\"teads\"></div>'
        paragraphs = response.xpath('/html/body/main/div[5]/div/div[1]').get()
        item['content'] = re.findall(pattern, paragraphs, re.DOTALL)[0].strip() # robust

        item['url'] = response.xpath('/html/head/link[3]/@href').get() # robust

        self.items.append(item)

    def closed(self, reason):
        json_path = 'almadina.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)