# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PakwheelsItem(scrapy.Item):
    car_name = scrapy.Field()
    car_model = scrapy.Field()
    car_model_date = scrapy.Field()
    car_description = scrapy.Field()
    car_conditions = scrapy.Field()
    car_fuel_type = scrapy.Field()
    car_price = scrapy.Field()
    car_price_currency = scrapy.Field()
    car_manufacturer = scrapy.Field()
    car_transmission_type = scrapy.Field()
    car_color = scrapy.Field()
    car_engine_capacity = scrapy.Field()
    car_mileage = scrapy.Field()
    car_url = scrapy.Field()
    
