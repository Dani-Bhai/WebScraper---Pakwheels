import scrapy
from ..items import PakwheelsItem
import json 

class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.pakwheels.com"]
    # start_urls = ["https://www.pakwheels.com/used-cars/search/-/ct_karachi/"]
    
    
    # 482 pages
    
    def start_requests(self):
        
        start_urls = []

        for p in range (1, 480):
            start_urls.append(f"https://www.pakwheels.com/used-cars/search/-/ct_karachi/?page={p}")

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    
    def parse_search_page(self, response):
        links = response.css("a.car-name.ad-detail-path::attr(href)").getall()
        for link in links:
            new_link = f"https://www.pakwheels.com{link}"
            yield scrapy.Request(url=new_link, callback=self.parse_item)

    

    def parse_item(self, response):
        item = PakwheelsItem()
        scripts = response.css("script[type='application/ld+json']") 
        if len(scripts) > 1:
            script = scripts[1]
            data = json.loads(script.css("::text").get())

            item["car_name"] = data["name"]
            item["car_model"] = data["model"]
            item["car_model_date"] = data["modelDate"]
            item["car_description"] = data["description"]
            item["car_conditions"] = data["itemCondition"]
            item["car_fuel_type"] = data["fuelType"]
            item["car_price"] = data["offers"]["price"]
            item["car_price_currency"] = data["offers"]["priceCurrency"]
            item["car_color"] = data["color"]
            item["car_manufacturer"] = data["manufacturer"]
            item["car_transmission_type"] = data["vehicleTransmission"] 
            item["car_engine_capacity"] = data["vehicleEngine"]["engineDisplacement"]
            item["car_mileage"] = data["mileageFromOdometer"]
            item["car_url"] = data["offers"]["url"]

            yield item









