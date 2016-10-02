#coding=utf-8
import re

if __name__ == '__main__':
    pattern = re.compile('^hello\d{3}$')

    result1 = re.match(pattern,'hello3')
    if result1:
        print result1.group()
    else:
        print 'result1 failed'

    result2 = re.match(pattern,'hello123')
    if(result2):
        print result2.group()
    else:
        print "result2 failed"

    result3 = re.match(pattern,'hello345')
    if result3:
        print result3.group()
    else:
        print 'result3 failed'


    result4 = re.match(r'(?P<id>\.*)','!123sfaasdf')
    if result4:
        print 'success',result4.group()
    else:
        print 'result4 failed'

    pattern = re.compile('<div class="title_all">.*?<font.*?>(.*?)</font>.*?<ul>(.*?)<tr>.*?<div id="Zoom">')
