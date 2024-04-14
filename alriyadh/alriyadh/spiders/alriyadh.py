from pathlib import Path
from scrapy.exceptions import CloseSpider
import scrapy
import json
import time



class Alriyadh(scrapy.Spider):
    name = "alriyadh"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 2070004
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):  # Change to this after first page 
            url = f'https://www.alriyadh.com/{i}'
            yield scrapy.Request(url=url, callback=self.parse)
            #time.sleep(5)  # Add a delay of 5 seconds between requests

    def parse(self, response):
        item = {}

        # Extract the title
        item['title'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/h2//text()').get().strip()

        # Extract the date
        item['date'] = response.css('.article-time time::text').get().strip()

        # Extract the content
        paragraphs = response.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/div[6]//text()').getall()
        item['content'] = ' '.join(paragraphs).strip()

        # Add the URL of the page
        item['url'] = response.url

        # Check for specific keywords in the content (if needed)
        self.items.append(item)

        # # Check if content is empty and stop the spider if it is
        # if not item['content'].strip():
        #     raise CloseSpider("Content is empty. Stopping spider.")


    def closed(self, reason):
        # Save the chapters as a JSON file
        json_path = 'alriyadh.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)