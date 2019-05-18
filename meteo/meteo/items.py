# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeteoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    latlon = scrapy.Field()
    region = scrapy.Field()
    province = scrapy.Field()
    locality = scrapy.Field()
    altitude = scrapy.Field()
    timestamp = scrapy.Field()
    temp = scrapy.Field()
    humidity = scrapy.Field()
    wind_address = scrapy.Field()
    wind_speed = scrapy.Field()
    pressure = scrapy.Field()
    sun = scrapy.Field()
    rain = scrapy.Field()

