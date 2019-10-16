# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from quotetutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    redis_key = 'quotes.toscrape:start_urls'

    def parse(self, response):
        quotes = response.css(".quote")
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()     #只有一个内容就可以用extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tags::text').extract()     #当有多个内容就用extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)        #response.urljoin()可以将括号内的参数添加到当前页面的url后面
        yield scrapy.Request(url=url, callback=self.parse)      #第一个参数URL 表示访问这个URL的页面，后面的参数表示调用自己的函数

