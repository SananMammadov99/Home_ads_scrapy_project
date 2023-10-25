# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class BinaAzItem(Item):
    # define the fields for your item here like:
    scraped_date = Field()
    title = Field()
    price_value = Field()
    price_currency = Field()
    url = Field()
    description = Field()
    last_updated = Field()
    number_of_views = Field()
    owner_name = Field()
    owner_region = Field()
    shop_owner_name = Field()
    shop_owner_region = Field()
    residence_name = Field()
    residence_region = Field()
    latitude = Field()
    longitude = Field()

 
    pass


class DynamicItem(Item):
    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = {}