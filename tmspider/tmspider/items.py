# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
     uid = scrapy.Field()
     name = scrapy.Field()
     age = scrapy.Field()
     photoUrl = scrapy.Field()

     # def __str__(self):
     #     return "{0}, {1}, {2}, {3}".format(uid, name, age, photoUrl)
