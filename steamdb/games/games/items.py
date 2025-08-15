# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GamesItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    overall_reviews = scrapy.Field()
    total_players = scrapy.Field()
    rating = scrapy.Field()
    supported_systems = scrapy.Field()
    technologies = scrapy.Field()