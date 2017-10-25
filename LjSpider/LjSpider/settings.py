# -*- coding: utf-8 -*-

# Scrapy settings for LjSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'LjSpider'

SPIDER_MODULES = ['LjSpider.spiders']
NEWSPIDER_MODULE = 'LjSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

RETRY_ENABLED = True
RETRY_TIMES = 25
RETRY_HTTP_CODES = [500,502,503,504,408,302]

# FEED_URI = '/home/nightheart/workspace/www/LianjiaSpider/LjSpider/esf_irt_2017-09-24.csv'
# FEED_URI = '/mnt/d/workspace/www/LianjiaSpider/LjSpider/deal_irt_2017-09.csv'
FEED_FORMAT = 'CSV'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# REDIRECT_ENABLED = False

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'LjSpider.middlewares.LjspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'LjSpider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# DOWNLOADER_MIDDLEWARES_BASE = {
#     'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
#     'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
#     'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
#     #'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
#     'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 800,
#     'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
#     'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'LjSpider.pipelines.CityPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_TIMEOUT = 4
# HTTPERROR_ALLOWED_CODES = [302,]

LOG_LEVEL = 'INFO'
