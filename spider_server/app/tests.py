#coding=utf-8
from django.test import TestCase
import datetime
# Create your tests here.
import re
if __name__ == '__main__':
    # pattern_Score = re.compile('类.*?别　(.*?)<br />')
    # str_data = '<br /><br />◎译　　名　爱丽丝梦游仙境2：镜中奇遇记/爱丽丝镜中奇遇记<br />◎片　　名　Alice Through the Looking Glass<br />◎年　　代　2016<br />◎国　　家　美国<br />◎类　　别　奇幻/冒险<br />◎语　　言　英语<br />◎字　　幕　中英双字幕<br />◎IMDb评分 6.4/10 from 23,814 users<br />◎文件格式　HD-RMVB<br />◎视频尺寸　1280 x 692<br />◎文件大小　1CD<br />◎片　　长　115分钟(中国大陆)/113分钟<br />◎导　　演　詹姆斯&middot;波宾 James Bobin<br />◎主　　演　约翰尼&middot;德普 Johnny Depp<br />　　　　　　米娅&middot;华希科沃斯卡 Mia Wasikowska<br />　　　　　　海伦娜&middot;伯翰&middot;卡特 Helena Bonham Carter<br />　　　　　　安妮&middot;海瑟薇 Anne Hathaway<br />　　　　　　萨莎&middot;拜伦&middot;科恩 Sacha Baron Cohen<br />　　　　　　瑞斯&middot;伊凡斯 Rhys Ifans<br />　　　　　　马特&middot;卢卡斯 Matt Lucas<br />　　　　　　琳赛&middot;邓肯 Lindsay Duncan<br />　　　　　　里奥&middot;比尔 Leo Bill<br />　　　　　　杰拉丁妮&middot;詹姆斯 Geraldine James<br />　　　　　　安德鲁&middot;斯科特 Andrew Scott<br />　　　　　　理查德&middot;阿米蒂奇 Richard Armitage<br />　　　　　　爱德华&middot;斯皮伊尔斯 Ed Speleers<br />　　　　　　艾伦&middot;瑞克曼 Alan Rickman<br />　　　　　　保罗&middot;怀特豪斯 Paul Whitehouse<br />　　　　　　斯蒂芬&middot;弗雷 Stephen Fry<br />　　　　　　马特&middot;沃格尔 Matt Vogel<br />　　　　　　芭芭拉&middot;温德索 Barbara Windsor<br />　　　　　　麦克&middot;辛 Michael Sheen<br />　　　　　　蒂莫西&middot;斯波 Timothy Spall<br />　　　　　　托比&middot;琼斯 Toby Jones<br /><br />◎简　　介<br /><br />　　爱丽丝（米娅&middot;华希科沃斯卡 Mia Wasikowska 饰）为了拯救挚友疯帽子（约翰尼&middot;德普 Johnny Depp 饰）而重返仙境，她与白皇后（安妮&middot;海瑟薇 Anne Hathaway 饰）及一群老朋友一起，展开了一段璀璨华美、永生难忘的奇幻冒险。然而除了邪恶的红皇后之外，爱丽丝还要面对另一位劲敌&mdash;&mdash;时间（萨莎&middot;拜伦&middot;科恩 Sacha Baron Cohen 饰），他是传说中无人能击败的角色！爱丽丝要如何才能扭转乾坤，拯救疯帽子和仙境世界？<br />　　影片改编自路易斯&middot;卡罗尔广受好评的同名原作。<br /><br />'
    # result = re.findall(pattern_Score,str_data)
    # if result:
    #     for item in result:
    #         print item
    # else:
    #     print('error')
    # movie_title_pattern = re.compile("《(.*?)》")
    # dst_str = "2016年奇幻《爱丽丝梦游仙境2：镜中奇遇记》"
    # result = re.findall(movie_title_pattern, dst_str)
    # if result:
    #     print(result[0])
    # else:
    #     print '其他'

    # removeComma = re.compile(',')
    # getCommaResult = re.findall(removeComma, '6,6')
    # if getCommaResult:
    #     print 'fasdfad'
    #     print float(re.sub(removeComma, ".", '6,6'))
    #
    # else:
    #     print float('6.6')

    # pattern = re.compile('(http.*?jpg).*?')
    # result = re.findall(pattern,"http://pic.yupoo.com/lihangze/DigGMbq8/ShhTp.jpg")
    # if result:
    #     print result[0]
    # else:
    #     print 'failed'

    # pattern = re.compile('.*?(\d{4}/\d{1,2}/\d{1,2})')
    pattern = re.compile('(.*?)\w{2}')
    result = re.findall(pattern, '终极硬汉BD1280高清国语中英双字')
    if result:
        print result[0]
        #releaseTime = datetime.datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        #return datetime.datetime(releaseTime.year, releaseTime.month, releaseTime.day)
    else:
        print 'errrerer'