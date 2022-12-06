# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    URL = scrapy.Field()
    Title = scrapy.Field()
    Description = scrapy.Field()
    Comments = scrapy.Field()
    Reply = scrapy.Field()
    Transcript = scrapy.Field()
