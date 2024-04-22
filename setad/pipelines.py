# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from email.quoprimime import header_check

from itemadapter import ItemAdapter

import pandas as pd


class SetadPipeline:

    I_data = []

    def process_item(self, item, spider):

        key = list(item)
        if key[0] == 'FP_data':
            df = pd.DataFrame(item['FP_data'])
            df.set_index("id42", inplace=True)
            df.to_csv("setadData.csv", encoding='utf-8')

        elif key[0] == 'I_data':
            self.I_data.append(item['I_data'])

        return item

    def close_spider(self, spider):

        df = pd.DataFrame(self.I_data)
        df.set_index("id1", inplace=True)

        df.to_csv("infos.csv", encoding='utf-8')
