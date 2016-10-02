#-*- coding:utf-8 -*-
__author__ = 'jclin'
import struct
from loglib.logApi import CSysLog

class MobileDataType(object):
    KEEP_ALIVE = 0x00,              #保活消息
    ENGINE_CHECK = 0x01,            #发动机体检
    ENGINE_CHECK_BACK = 0x02,       #发动机体检结果
    BRAKE_CHECK = 0x03,             #刹车体检
    BRAKE_CHECK_BACK = 0x04,        #刹车体检结果
    TRANSMISSION_CHECK = 0x05,      #变速箱体检
    TRANSMISSION_CHECK_BACK = 0x06, #变速箱体检结果
    GASBAG_CHECK = 0x07,            #气囊体检
    GASBAG_CHECK_BACK = 0x08,       #气囊体检结果

class FrameMobile(object):
    def __init__(self):
        self.device_id = bytearray(10)
        self.payload_len = 0
        self.data_payload = bytearray()
        self.messageNum = 0
        self.head = 'ck'
        self.messages = []

    def set_data(self,data):
        self.data_payload = bytearray(data)
        self.device_id = str(self.data_payload[2:12])
        self.messageNum = self.data_payload[13]
        for index in range(self.messageNum):
            self.messages.append([self.data_payload[14+2*index],self.data_payload[15+index*2]])

    def set_device_id(self,device_id):
        self.device_id = device_id

    def add_message(self,message):
        '''
        message:[messagetype,value]
        '''
        if isinstance(message,list) and len(message) == 2:
            self.messageNum +=1
            self.messages.append(message[0])
            self.messages.append(message[1])
        else:
            CSysLog.error('add_message error format message')

    def format_to_bytearray(self):
        pass

    def get_device_id(self):
        return self.device_id

class DataType(object):
    CAR_DATA = 0x00 #车辆数据传输
    GPS_DATA = 0x01 #GPS传输数据
    UP_DATA = 0x02  #上报数据传输
    HEART_BEAT_DATA = 0x03 #心跳交互数据
    FILE_DATA = 0x04    #文件传输


class FrameType:
    MSG_TYPE_CONNECT = 0x01  # 设备需要先与服务器建立会话，发送CONNECT 消息并带上相应参数，服务器收到请求后做出是否建立会话的判断
    MSG_TYPE_CONNACK = 0x02  # Connect Acknowledgment设备发竤CONNECT 消息后等待服务器是否同意建立会话，通过回复CONNACK 消息给设备。
    MSG_TYPE_PUBLISH = 0x03  # 成功建立会话后双方可以相互主动发送消息， 业务消息通过PUBLISH 包承载
    MSG_TYPE_PUBACK = 0x04  # 双方对PUBLISH 包数据的回复
    MSG_TYPE_PINGREQ = 0x0C #心跳消息通过PING 相关包承载
    MSG_TYPE_PINGRESP = 0x0D  # 回复PING 包的相关数据
    MSG_TYPE_DISCONNECT = 0x0E  # 结束会话通过DISCONNECT 消息达成

class DataTypeMajor:
    JOURNEY_DATA = 0x00 #上报行程数据。包括：着车，熄火，汇总数据
    DRIVING_BEHAVIOR_DATA =  0x01#上报驾驶行为数据。包括：急加，急减，急转弯，怠速过长，疲劳驾驶，超速
    GPS_DATA = 0x02 #上报GPS数据
    CAR_DATA = 0x03#上报车辆数据。包括：VIN，数据流
    DEVICE_INFO_DATA = 0x04#上报终端设备信息数据。包括：IMSI，设备故障，休眠，唤醒，长时间未定位。
    CAR_SAFE_DATA = 0x05#上报车辆安全数据。包括：故障码，低电压，熄火后振动，低水温高转速，拖车，疑似碰撞，疑似翻车
    #0x06 - 0xEF#保留
    OBD_DEVICE_REQ = 0xF0#设备请求服务器数据
    SERVICE_REQ = 0xF1#服务器请设备数据

class DeviceType:
    UPGRADE = 0x00 #设备升级
    VEHICLE_CHECKUP = 0x01#车辆体检
    QUERY_PARAM = 0x03 #查询参数
    QUERY_LOG_DATA = 0x04 #查询log数据
    TRANSMISSION_DATA_FRAME = 0x05 #透传数据帧
    SET_CAR_INFO = 0x06 #设置车辆信息
    #0x07 - 0x7D保留
    REBOOT_DEVICE = 0x7E #设备重启
    KEEP_SESSION = 0x7F #无具体意义，仅用于服务器保持会话

class FrameBase(object):
    """
    |帧头|帧序号|终端编号|数据类型|数据长度|有效数据|异或校验|帧尾巴|
    |2  |2      |   10    | 1     | 2     |    N    |  1     |  2  |
    采用大端方式传输int
    """


    def __init__(self):
        self.head_payload = bytearray(17)
        #Frame Head 字段
        self.frame_head = '\x55\x55'
        self.frame_index= bytearray(2)
        self.device_id = bytearray(10)
        self.frame_type = bytearray(1)
        self.payload_len = bytearray(2)
        #有效数据

        self.data_payload = bytearray()

        #帧尾字段
        self.check_num = '\xAB'
        self.frame_tail = '\xAA\xAA'

        self.head_len = 17
        self.frame_tail_len = 3

    def set_head_data(self,head_data):
        self.head_payload = bytearray(head_data)
        self.frame_head = self.head_payload[0:2]
        self.frame_index = self.head_payload[2:4]#self.head_payload[2] << 8 | self.head_payload[3]
        self.device_id = self.head_payload[4:14]
        self.frame_type =self.head_payload[14]
        self.payload_len = self.head_payload[15:17]
        return self.check_valid_head()

    def check_valid_head(self):
        if self.frame_head[0] == 0x55 and self.frame_head[1] == 0x55:
            return True
        else:
            return False

    def set_data_payload(self,payload_data):
        self.data_payload = payload_data

    def get_device_id(self):
        return str(self.device_id)

    def get_frame_head(self):
        return self.frame_head

    def get_frame_index(self):
        return str(self.frame_index)

    def get_data_type(self):
        return  self.frame_type

    def get_payload_len(self):
        return self.payload_len[0] << 8 | self.payload_len[1]

    def get_payload(self):
        return self.data_payload

    def init_send_frame(self):
        '''
        初始化帧头基本信息
        '''
        pass


    def set_frame_index(self,index):
        self.frame_index = bytearray(index)

    def set_device_id(self,id):
        self.device_id = bytearray(id)

    def set_frame_type(self,type):
        '''
        设置帧类型:
        MSG_TYPE_CONNECT 0x01 Client request to connect to Server
        设备需要先与服务器建立会话，发送CONNECT 消
        息并带上相应参数，服务器收到请求后做出是否建
        立会话的判断
        MSG_TYPE_CONNACK 0x02 Connect Acknowledgment
        设备发竤CONNECT 消息后等待服务器是否同意建
        立会话，通过回复CONNACK 消息给设备。
        MSG_TYPE_PUBLISH 0x03 Publish message
        成功建立会话后双方可以相互主动发送消息， 业
        务消息通过PUBLISH 包承载
        MSG_TYPE_PUBACK 0x04 Publish Acknowledgment
        双方对PUBLISH 包数据的回复
        MSG_TYPE_Reserved5-11 0x05...0x0B Reserved
        MSG_TYPE_PINGREQ 0x0C PING Request
        心跳消息通过PING 相关包承载
        MSG_TYPE_PINGRESP 0x0D PING Response
        回复PING 包的相关数据
        MSG_TYPE_DISCONNECT 0x0E Client is Disconnecting
        结束会话通过DISCONNECT 消息达成
        :param type:
        :return:
        '''
        self.frame_type=bytearray(type)

    def set_payload_len(self,length):
        self.payload_len = bytearray(length)

    def set_payload(self,payload):
        self.data_payload = bytearray(payload)

    def set_check_num(self,checkNum):
        self.check_num = checkNum

    def frame_to_byte_arrary(self):

        # fmt = '!2s' + '2s' + '10s' + 's' + '2s' + str(len(self.data_payload)) + 's' + 's' + '2s'
        # print 'data :%d %d %d %d %d %d %d %d'%(len(self.frame_head),len(self.frame_index),len(self.device_id),len(self.frame_type),len(self.payload_len),len(self.data_payload),len(self.check_num),len(self.frame_tail))
        # print fmt
        return str(self.frame_head) + str(self.frame_index) + str(self.device_id) + str(self.frame_type) + str(self.payload_len) + str(self.data_payload) +str(self.check_num) +str(self.frame_tail)

