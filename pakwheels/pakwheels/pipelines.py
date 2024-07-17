# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import csv
import os

class PakwheelsPipeline:
    def process_item(self, item, spider):
        return item



class SQLiteNoDupesPipeline:
    def __init__(self) -> None:
        self.con = sqlite3.connect("product.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products(
                name,
                model,
                model_date,
                description,
                conditions,
                fuel_type,
                price,
                price_currency,
                manufacturer,
                transmission_type,
                color,
                engine_capacity,
                mileage,
                url
            ) 
            """
        )
        self.csv_file = open('products.csv', 'a', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        
        if os.stat('products.csv').st_size == 0:
            self.csv_writer.writerow([
                'name', 'model', 'model_date', 'description', 'conditions',
                'fuel_type', 'price', 'price_currency', 'manufacturer',
                'transmission_type', 'color', 'engine_capacity', 'mileage', 'url'
            ])

    def process_item(self, item, spider):
        self.cur.execute(
        "SELECT * FROM products WHERE url = ?", (item["car_url"],)  
        )

        result = self.cur.fetchone()

        if result:
            spider.logger.warn(f"Item already in DB {item['car_url']}")

        else:
            self.cur.execute(
            """ INSERT INTO products(name,model,model_date,description,conditions,fuel_type,price,price_currency,manufacturer,transmission_type,color,engine_capacity,mileage,url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)""",(
                item["car_name"],
                item["car_model"],
                item["car_model_date"],
                item["car_description"],
                item["car_conditions"],
                item["car_fuel_type"],
                item["car_price"],
                item["car_price_currency"],
                item["car_manufacturer"],
                item["car_transmission_type"],
                item["car_color"],
                item["car_engine_capacity"],
                item["car_mileage"],
                item["car_url"]
                ),
            )

            self.con.commit()
            self.csv_writer.writerow([
                item["car_name"], item["car_model"], item["car_model_date"],
                item["car_description"], item["car_conditions"],
                item["car_fuel_type"], item["car_price"], 
                item["car_price_currency"], item["car_manufacturer"],
                item["car_transmission_type"], item["car_color"],
                item["car_engine_capacity"], item["car_mileage"], 
                item["car_url"]
            ])
            return item

