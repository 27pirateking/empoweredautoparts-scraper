# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmpoweredautopartsItem(scrapy.Item):
    # define the fields for your item here like:
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    sku = scrapy.Field()
    current_price = scrapy.Field()
    actual_price = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    compatible_models = scrapy.Field()
    features = scrapy.Field()
    product_highlights = scrapy.Field()
    product_specifications = scrapy.Field()
    you_are_buying = scrapy.Field()
    specification = scrapy.Field()
    pass