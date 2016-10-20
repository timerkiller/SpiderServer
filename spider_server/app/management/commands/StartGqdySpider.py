#coding=utf-8
from django.core.management.base import BaseCommand
from app.spider.gqdy_spider import GqdySpider
from loglib.logApi import CSysLog

class Command(BaseCommand):
    def handle(self, *args, **options):
        CSysLog.info('start get home data')
        GqdySpider.start(0x01)
        try:
            GqdySpider.write_all_data_to_database()
        except Exception, e:
            CSysLog.info('write data to datebase error :%s ', e)

        # CSysLog.info('start get page url')
        # GqdySpider.start_all()
        # try:
        #     GqdySpider.write_to_database(GqdySpider.DataType.NEW_MOV)
        # except Exception, e:
        #     CSysLog.info('write data to datebase error :%s ', e)