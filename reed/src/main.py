from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apify import Actor

from .pipelines import ActorDatasetPushPipeline,MySQLPipeline

from .spiders.reed import reed


async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        # max_depth = actor_input.get('max_depth', 1)
        start_urls = [start_url.get('url') for start_url in actor_input.get('start_urls', [{ 'url': 'https://www.reed.co.uk' }])]

        # database stuff

        MYSQL_HOST = actor_input.get('MYSQL_HOST')
        MYSQL_DB_NAME = actor_input.get('MYSQL_DB_NAME')
        MYSQL_USER = actor_input.get('MYSQL_USER')
        MYSQL_PASSWORD = actor_input.get('MYSQL_PASSWORD')

        proxy_settings = actor_input.get('proxySettings')
        proxy_configuration = await Actor.create_proxy_configuration(actor_proxy_input=proxy_settings)
        proxy_url = await proxy_configuration.new_url()
        proxies_list = []
        
        for i in range(1000):
            proxies_list.append(await proxy_configuration.new_url())



        settings = get_project_settings()
        settings['ITEM_PIPELINES'] = { MySQLPipeline : 400 }
        
        settings['MYSQL_HOST'] = MYSQL_HOST
        settings['MYSQL_DB_NAME'] = MYSQL_DB_NAME
        settings['MYSQL_USER'] = MYSQL_USER
        settings['MYSQL_PASSWORD'] = MYSQL_PASSWORD

        settings['proxies_list'] = proxies_list
    

        process = CrawlerProcess(settings)
        # If you want to run multiple spiders, call `process.crawl` for each of them here
        process.crawl(reed)

        process.start()
