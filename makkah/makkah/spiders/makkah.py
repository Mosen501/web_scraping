import re
import scrapy
import json
class makkah(scrapy.Spider):
    name = "makkah"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.first_page = 1
        self.latest_page = 1614475
    def start_requests(self):
        for i in range(self.first_page,self.latest_page+1):
            url = f'https://makkahnewspaper.com/article/{i}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}

        item['title'] = response.xpath('/html/body/main/div[4]/div/div[1]/div[1]/div[2]/h1/text()').get() # robust

        item['date'] = response.xpath('/html/head/meta[19]/@content').get() # robust

        pattern = r'class="article-desc">(.*?)class="article_tags">'
        paragraphs = response.xpath('/html/body/main/div[4]').get()
        item['content'] = re.findall(pattern, paragraphs, re.DOTALL)[0].strip() # robust

        item['url'] = response.xpath('/html/head/link[3]/@href').get() # robust

        self.items.append(item)

    def closed(self, reason):
        json_path = 'makkah.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)