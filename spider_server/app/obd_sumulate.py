# coding=utf-8
__author__ = 'Administrator'
from socket import *
import struct

FRAME_HEADER = '\x55\x55'
# FRAME_INDEX='\x00\x01'
FRAME_INDEX_INT = 0x00
TERMINAL_INDEX = '\x58\x48\x11\x01\x15\x10\x09\x01\x23\x45'
# DATA_LEN='\x00\x00'
DATA_LEN = 0x00
FRAME_TAIL = '\xAA\xAA'

SOFT_VER = '\x00\x01'


class dataType(object):
    MSG_TYPE_CONNECT ='\x01'
    CAR_DATA = '\x00'  # 车辆数据传输
    GPS_DATA = '\x01'  # GPS传输数据
    UP_DATA = '\x02'  # 上报数据传输
    HEART_BEAT_DATA = '\x03'  # 心跳交互数据
    FILE_DATA = '\x04'  # 文件传输


class heartReqType(object):
    TIME_SYNEC = '\x00'  # 时间同步
    ORDER_REQ = '\x01'  # 命令申请
    ORDER_RES = '\x02'  # 命令回应
    AGPS_REQ = '\x03'  # Agps 请求


class oderReqType(object):
    None_TEST = '\x00'
    CAR_TEST = '\x01'
    CLEAR_WRONG_CODE = '\x02'
    PARR_SET = '\x03'
    SOFT_UP = '\x04'


def combinmsg(*arg):
    msg = ''
    for i in arg:
        # print i
        msg += chr(i)
    return msg


host = '127.0.0.1'
port = 25089
bufsize = 1024
import time

addr = (host, port)
client = socket(AF_INET, SOCK_STREAM)
client.connect(addr)

while True:
     # 帧序号 2byte short
    FRAME_INDEX_INT = FRAME_INDEX_INT + 1
    FRAME_INDEX = struct.pack('!H', FRAME_INDEX_INT)
    checkstr = FRAME_INDEX + TERMINAL_INDEX
    msg = (FRAME_HEADER + FRAME_INDEX + TERMINAL_INDEX)
    question1 = """
    选择数据类型:
     0 车辆数据传输
     1 GPS数据传输
     2 上报数据传输
     3 心跳交互通信
     4 文件传输
     5 会话建立
    """
    dataTypeSelect = input(question1)
    dataTypeSelect = int(dataTypeSelect)
    if dataTypeSelect==5:
        msg+=dataType.MSG_TYPE_CONNECT
        checkstr+=dataType.MSG_TYPE_CONNECT
        portocolver='\x01'
        preframenum='\x00\x11'
        equver='\x02\x34\x02\x01'
        dbver='\x02\x01'
        payload=portocolver+preframenum+equver+dbver

    elif dataTypeSelect==0:
        msg += dataType.CAR_DATA
        #format
        # time | avspeed | max speed | minspeed | youhao | mile | fenduancount | fenduandata  | jiashicount | jiashixingwei
        # 4         1         1            1        2       2           1        (1|1|2|2 *n ) (0|0|3|3)   1   (1|1|(4*M))*N
        time="\x21\x22\x23\x24"
        avspeed="\x40"
        maxspeed="\x50"
        minspeed="\x20"
        youhao="\xa0\xa0"
        mile="\xa0\xa0"
        fengduancount="\x01"
        fenduandata1="\x01"
        fenduandata2="\xa0"
        fenduandata3="\xb0"
        fenduandata4="\xc0"
        jiashicount="\x02"
        jiashidata11="\x0A"
        jiashidata12="\x02"
        jiashidata13="\x21\x22\x23\x24\x21\x22\x23\x24"
        jiashidata21="\x0B"
        jiashidata22="\x01"
        jiashidata23="\x21\x22\x23\x24"
        payload = time+avspeed+maxspeed+minspeed+youhao+mile+fengduancount+fenduandata1+fenduandata2+fenduandata3+fenduandata4+jiashicount+jiashidata11+jiashidata12+jiashidata13+jiashidata21+jiashidata22+jiashidata23
    elif dataTypeSelect==1:
        msg += dataType.GPS_DATA
        #format
        # count | gpsinfo|
        # 1     | (4|1|4|1|4)*N
        gpscount ="\x02"
        gps1latitude="\x01\x02\x03\x04"
        gps1sn="\x00"
        gps1longitude="\x01\x02\x03\x04"
        gps1ew="\x00"
        gps2latitude="\x01\x02\x03\x04"
        gps2sn="\x00"
        gps2longitude="\x01\x02\x03\x04"
        gps2ew="\x00"
        payload=gpscount+gps1latitude+gps1sn+gps1longitude+gps1ew+gps2latitude+gps2sn+gps2longitude+gps2ew
        pass
    elif dataTypeSelect==2:
        msg += dataType.UP_DATA
        question2 = """
        选择数据上报类型:
        1 着车后故障
        2 熄火上报
        3 低电压上报
        4 熄火后震动上报
        5 上电上报
        6 车辆识别码VIN上报
        7 sim卡标识IMSI上报
        """
        upTypeSelect = input(question2)
        upTypeSelect = int(upTypeSelect)
        if upTypeSelect == 1:
            uptype="\x01"
            time="\x21\x22\x23\x24"
            count="\x02"
            errorcode="\x00\x00\x01\x00\x00\x02"
            payload =uptype+time+count+errorcode
            pass
        elif upTypeSelect ==2:
            uptype="\x02"
            time="\x21\x22\x23\x24"
            payload=uptype+time
            pass
        elif upTypeSelect ==3:
            uptype="\x03"
            time="\x21\x22\x23\x24"
            voltage="\x0a"
            payload=uptype+time+voltage
            pass
        elif upTypeSelect ==4:
            uptype="\x04"
            time="\x21\x22\x23\x24"
            payload=uptype+time
            pass
        elif upTypeSelect ==5:
            uptype="\x05"
            time="\x21\x22\x23\x24"
            payload=uptype+time
            pass
        elif upTypeSelect==6:
            uptype="\x06"
            time="\x21\x22\x23\x24"
            vin="\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17"
            payload=uptype+time+vin
            pass
        elif upTypeSelect==7:
            uptype="\x07"
            time="\x21\x22\x23\x24"
            vin="\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15"
            payload=uptype+time+vin
            pass
        else:
            print "error input"
            break
        pass



    elif dataTypeSelect == 3:
        msg += dataType.HEART_BEAT_DATA
        question2 = """
        选心跳择交互通信类型:
        0 时间同步
        1 命令申请
        2 命令回应
        3 Agps请求
        """
        heartSelect = input(question2)
        heartSelect = int(heartSelect)
        if heartSelect == 0:
            # TIME SYNC
            payload = heartReqType.TIME_SYNEC
        elif heartSelect == 1:
            question3 = """
            选心命令申请类型:
            0 无
            1 车辆体检
            2 清除故障码
            3 参数设定
            4 软件升级
            """
            orderReqSelect=int(input(question3))
            if orderReqSelect==0:
                pass
            elif orderReqSelect==1:
                payload = (heartReqType.ORDER_REQ + oderReqType.CAR_TEST)
                pass
            elif orderReqSelect==2:
                payload = (heartReqType.ORDER_REQ + oderReqType.CLEAR_WRONG_CODE)
                pass
            elif orderReqSelect==3:
                payload = (heartReqType.ORDER_REQ, oderReqType.PARR_SET)
                pass
            elif orderReqSelect==4:
                payload = (heartReqType.ORDER_REQ + oderReqType.SOFT_UP + SOFT_VER)
                pass
            payload = (heartReqType.ORDER_REQ + oderReqType.SOFT_UP + SOFT_VER)
        elif heartSelect == 2:
            payload=heartReqType.ORDER_RES
            #orderresponse
            pass
        elif heartSelect == 3:
            # ORDER ARGS
            pass
            # payload = chr(heartReqType.ORDER_RES)+
            # msg = struct.pack('s',s)


    DATA_LEN = len(payload)
    if (DATA_LEN > 516):
        print 'over max-length'
        break
    # DATA_LEN=str(DATA_LEN)
    import binascii
    print binascii.b2a_hex(payload)
    DATA_LEN = struct.pack('!H', DATA_LEN)
    checkstr+=payload
    check='\xAB'
    # for i in range(2+10+1+2+len(payload)):
    #     check=check^checkstr[i]
    msg +=  DATA_LEN + payload +check + FRAME_TAIL
    print msg
    print binascii.b2a_hex(msg)
    # msg='a'
    client.send(msg)
    data = client.recv(bufsize)
    print "receive data:",(data.decode())
    # time.sleep(3)

client.close()
