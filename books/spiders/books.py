# -*- coding: utf-8 -*-
import scrapy
import re

class BooksSpider(scrapy.Spider):
    name = 'books'
    def start_requests(self):
        for i in range(1,859841):
            url = 'https://www.zuijuzi.com/ju/' + str(i)
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        item = {}
        id = response.url.split("/")[-1]
        lines = response.css("div.content::text").getall()
        content = []
        for line in lines:
            content.append(line.strip())
        metas = response.css("div.info a").getall()
        tags = []
        writer = {}
        article = {}
        for meta in metas:
            tagResult = re.search('<a.*?href=".*tag/(.*?).html">(.*?)</a>', meta, re.S)
            if tagResult:
               tag = {}
               tag["id"] = tagResult.group(1)
               tag["title"] = tagResult.group(2)
               tags.append(tag)

            writerResult = re.search('<a.*?href=".*writer/(.*?)">(.*?)</a>', meta, re.S)
            if writerResult:
                if writerResult.group(1):
                    writer["id"] = writerResult.group(1)
                    writer["title"] = writerResult.group(2)
                
            articleResult = re.search('<a.*?href=".*article/(.*?)">(.*?)</a>', meta, re.S)
            if articleResult:
                article["id"] = articleResult.group(1)
                article["title"] = articleResult.group(2)       

        img = response.css("div.col-md-2 a img::attr(src)").get()
        if img:
            article['cover'] = img
        item["tags"] = tags
        item["writer"] = writer
        item["article"] = article
        item["id"] = id
        item["content"] = content
        yield item    
