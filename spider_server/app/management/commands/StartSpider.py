#coding=utf-8
from django.core.management.base import BaseCommand
from app.spider.dytt_spider import DyttSpider
from loglib.logApi import CSysLog
class Command(BaseCommand):
    def handle(self, *args, **options):
        CSysLog.info('start get home data')
        DyttSpider.start(0x00)
        try:
            DyttSpider.write_to_database(DyttSpider.DataType.HOME_PAGE)
        except Exception, e:
            CSysLog.info('write data to datebase error :%s ', e)

        CSysLog.info('start get page url')
        DyttSpider.start_all()
        try:
            DyttSpider.write_to_database(DyttSpider.DataType.NEW_MOV)
        except Exception, e:
            CSysLog.info('write data to datebase error :%s ', e)