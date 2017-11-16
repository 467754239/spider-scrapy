# -*- coding: utf-8 -*-
import scrapy

from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    #start_urls = ['http://tencent.com/']

    baseURL = "http://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        #node_list = response.xpath("//tbody/tr[@class='even']/td or //tbody/tr[@class='odd']/td")
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:

            try:
                item = TencentItem()
                # 提取每个职位信息，并且将提取出的Unicode字符编码为UTF-8
                item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0].encode('utf-8')
                item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0].encode('utf-8')
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0].encode('utf-8')
                item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0].encode('utf-8')
                item['workLocation'] = node.xpath("./td[4]/text()").extract()[0].encode('utf-8')
                item['publishTime'] = node.xpath("./td[5]/text()").extract()[0].encode('utf-8')
            except IndexError as e:
                item['positionType'] = "" 

            # 返回给管道 交给管道来处理
            yield item

        #if self.offset < 2550:
        #    self.offset += 10
        #    next_url = self.baseURL + str(self.offset)
        #    yield scrapy.Request(next_url, callback=self.parse)

        if len(response.xpath("//a[@class='noactive' and @id='next']")) == 0:
            next_url = "http://hr.tencent.com/" + response.xpath("//a[@id='next']/@href").extract()[0]
            print next_url
            #yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
            yield scrapy.Request(next_url, callback=self.parse)
