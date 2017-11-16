# -*- coding: utf-8 -*-
import scrapy
import json

from Douyu.items import DouyuItem

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']

    baseURL = "https://www.douyu.com/api/v1/getVerticalRoom?limit=20&offset="
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        print '>>>>>>>>>>>>>>>response.url: ', response.url
        data_list = json.loads(response.body)['data']
        if len(data_list) == 0:
            print '=' * 30
            return

        for data in data_list:
            item = DouyuItem()
            item['nickname'] = data['nickname']
            item['imagelink'] = data['vertical_src']
            yield item

        # 发送API的请求
        self.offset += 20
        next_url = self.baseURL + str(self.offset)
        print "--------------------", next_url
        yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
