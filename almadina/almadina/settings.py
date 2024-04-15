import sys

BOT_NAME = 'almadina'

SPIDER_MODULES = ['almadina.spiders']
NEWSPIDER_MODULE = 'almadina.spiders'

ROBOTSTXT_OBEY = True

sys.dont_write_bytecode = True

# custom_settings = {
#     'DOWNLOAD_DELAY': 1,  # Decreased download delay for faster scraping
#     'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Increased concurrent requests
#     # 'AUTOTHROTTLE_ENABLED': True,  # Enabled AutoThrottle extension
#     # 'AUTOTHROTTLE_START_DELAY': 2,  # Initial delay for AutoThrottle
#     # 'AUTOTHROTTLE_MAX_DELAY': 2,  # Maximum delay for AutoThrottle
#     # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,  # Target concurrency for AutoThrottle
# }