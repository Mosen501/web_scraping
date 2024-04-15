from pathlib import Path
import scrapy
import json
import time



class makkah(scrapy.Spider):
    name = "makkah"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 1611369
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):
            url = f'https://makkahnewspaper.com/article/{i}'
            yield scrapy.Request(url=url, callback=self.parse)
            #time.sleep(5)  # Add a delay of 5 seconds between requests

    def parse(self, response):
        item = {}

        item['title'] = response.xpath('/html/body/main/div[4]/div/div[1]/div[1]/div[2]/h1/text()').get()

        date = response.xpath('/html/body/main/div[4]/div/div[1]/div[1]/div[3]/div/p[2]/text()').get()
        if date is None or not date.strip():  # Check if date is empty or whitespace
            item['date'] = response.xpath('/html/body/main/div[4]/div/div[1]/div[1]/div[5]/div/p[2]/text()').get()
        else:
            item['date'] = date

        # Extract the content
        paragraphs = ' '.join(response.xpath('/html/body/main/div[4]/div/div[1]/div[2]/div[2]/p//text()').getall()).strip()
        if paragraphs is not paragraphs or not ''.join(paragraphs).strip():
             item['content'] = ' '.join(response.xpath('/html/body/main/div[4]/div/div[1]/div[1]/div[3]//text()').getall()).strip()
        else:
            item['content'] = paragraphs

        item['url'] = response.xpath('/html/head/link[3]/@href').get()

        self.items.append(item)
        # # Check if content is empty and stop the spider
        # if not item['content'].strip():
        #     raise CloseSpider("Content is empty. Stopping spider.")

    def closed(self, reason):
        json_path = 'makkah.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)