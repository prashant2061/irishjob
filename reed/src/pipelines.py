# Define your item pipelines here
#
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from apify import Actor
from itemadapter import ItemAdapter
import mysql.connector


# Used to output the items into the actor's default dataset
# Enabled only when the project is run as an actor
class ActorDatasetPushPipeline:
    async def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        await Actor.push_data(item_dict)
        return item


class MySQLPipeline:

    def open_spider(self, spider):
        print('Hello from pipeline')
        self.connection = mysql.connector.connect(
            host=spider.settings.get('MYSQL_HOST'),
            user=spider.settings.get('MYSQL_USER'),
            password=spider.settings.get('MYSQL_PASSWORD'),
            database=spider.settings.get('MYSQL_DB_NAME'),
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    async def process_item(self, item, spider):
        self.insert_data(item)
        await Actor.push_data(item)
        return item

    def insert_data(self, item):

        columns = [
        "url","job_title","salary","contract_type","job_type","location","posted_on_refreshed_on","application_link","closing_date","job_description","job_poster"

        ]
     
        data = tuple(item[column] for column in columns)
        print(f'This is the data OK! {data}')
        insert_sql = '''
            INSERT INTO adverts_table (
            url,job_title,salary,contract_type,job_type,location,posted_on_refreshed_on,application_link,closing_date,job_description,job_poster
            )
            VALUES (%s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s);
        '''

        self.cursor.execute(insert_sql, data)
        self.connection.commit()
