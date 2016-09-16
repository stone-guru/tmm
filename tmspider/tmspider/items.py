# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ModelBrief:
     def __init__(self):
        self.uid = ""
        self.name = ""
        self.age = ""
        self.photoUrl = ""

     def __str__(self):
         return "{0}, {1}, {2}, {3}".format(self.uid, self.name, self.age, self.photoUrl)

class TmmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
     uid = scrapy.Field()
     name = scrapy.Field()
     birthDate = scrapy.Field()
     city = scrapy.Field()
     waist = scrapy.Field()
     bust = scrapy.Field()
     hip = scrapy.Field()
     cup = scrapy.Field()
     height = scrapy.Field()
     weight = scrapy.Field()
