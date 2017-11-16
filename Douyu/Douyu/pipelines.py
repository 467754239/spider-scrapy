# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline


class DouyuPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_link = item['imagelink']
        yield scrapy.Request(image_link)

    def item_completed(self, results, item, info):
         image_path = [ x['path'] for ok, x in results if ok ]

         src_name = images_store + image_path[0]
         old_name = images_store + item['nickname'] + '.jpg'
         os.rename(src_name, old_name)

         return item
