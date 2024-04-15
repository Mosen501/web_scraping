from pathlib import Path
import scrapy
import json

class okaz(scrapy.Spider):
    name = "okaz"

    custom_settings = {
    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 2159581
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):
            url = f'https://www.okaz.com.sa/ampArticle/{i}'
            yield scrapy.Request(url=url, callback=self.parse)
            # time.sleep(1)  # Add a delay of 5 seconds between requests

    def parse(self, response):
        item = {}

        item['title'] = response.xpath('/html/body/div[3]/main/div/h1[1]//text()').get().strip()

        date = response.xpath('/html/body/div[3]/main/div/p[1]/span[2]//text()').get().strip()
        # if date is None or not date.strip():  # Check if date is empty or whitespace
        #     item['date'] = response.xpath('/html/body/div[3]/main/div/p[1]/span[2]//text()').get().strip()
        # else:
        item['date'] = date

        # Extract the content
        paragraphs = ' '.join(response.xpath('/html/body/div[3]/main/div/div[2]//text()').getall()).strip()
        # if paragraphs is not paragraphs or not ''.join(paragraphs).strip():
        #      item['content'] = ' '.join(response.xpath('/html/body/div[3]/main/div/div[2]//text()').getall()).strip()
        # else:
        item['content'] = paragraphs

        item['url'] = response.xpath('/html/head/link/@href').get().strip()

        self.items.append(item)
        # # Check if content is empty and stop the spider
        # if not item['content'].strip():
        #     raise CloseSpider("Content is empty. Stopping spider.")

    def closed(self, reason):
        json_path = 'okaz.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)