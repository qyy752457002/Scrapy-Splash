# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class SplashProjectPipeline:
    def __init__(self):
        self.data = {"Date": [], "Home Team": [], "Score": [], "Away Team": []}

    def process_item(self, item, spider):
        self.data["Date"].append(item.get("date"))
        self.data["Home Team"].append(item.get("home_team"))
        self.data["Score"].append(item.get("score"))
        self.data["Away Team"].append(item.get("away_team"))
        return item
    
    def close_spider(self, spider):
        df = pd.DataFrame(self.data)
        df.to_csv(r"./splash_output.csv", index=False)


