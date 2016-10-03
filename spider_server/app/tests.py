#coding=utf-8
from django.test import TestCase
import datetime
# Create your tests here.
import re
if __name__ == '__main__':
    pattern = re.compile('(\d{4}-\d{1,2}-\d{1,2}$)')
    result = re.findall(pattern,'你好吗2016-09-20')
    print datetime.datetime.today().strftime('%Y-%m-%d')
    if result:
        print result[0]
    else:
        print('error')