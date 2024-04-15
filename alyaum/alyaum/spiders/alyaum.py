from pathlib import Path
import scrapy
import json

class alyaum(scrapy.Spider):
    name = "alyaum"

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 200,  # Increased concurrent requests
    #     'AUTOTHROTTLE_ENABLED': True,  # Enabled AutoThrottle extension
    #     'AUTOTHROTTLE_START_DELAY': .1,  # Initial delay for AutoThrottle
    #     'AUTOTHROTTLE_MAX_DELAY': .3,  # Maximum delay for AutoThrottle
    #     'AUTOTHROTTLE_TARGET_CONCURRENCY': 200,  # Target concurrency for AutoThrottle
    # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 6524598
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):
            url = f'https://www.alyaum.com/article/{i}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
       
        item['title'] = response.xpath('/html/head/meta[19]/@content').get()

        date = response.xpath('/html/head/meta[13]/@content').get()
        item['date'] = date 

        # Extract the content
        paragraphs = ' '.join(response.xpath('/html/body/section/div[2]/div/div[1]/div[1]/div/div/div[5]/article/div/text()').getall()).strip()
        if paragraphs is not paragraphs or not ''.join(paragraphs).strip():
             item['content'] = ' '.join(response.xpath('/html/body/section/div[2]/div/div[1]/div[1]/div/div/div[4]/article/div/text()').getall()).strip()
        else:
            item['content'] = paragraphs

        item['url'] = response.xpath('/html/head/link[13]/@href').get()

        self.items.append(item)

    def closed(self, reason):
        json_path = 'alyaum.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)