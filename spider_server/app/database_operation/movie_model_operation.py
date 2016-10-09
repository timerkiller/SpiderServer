#coding=utf-8
import threading
from app.models import MovieModel
from loglib.logApi import CSysLog
from utilapp.tools import CTimeHelper
from django.utils import timezone
import datetime

class MovieModelOperation(object):
    '''
    movie 影视数据库操作类，所有该模型的数据库操作可以通过类操作
    '''
    objs = {}
    objs_locker = threading.Lock()
    def __new__(cls, *args, **kv):
        if cls in cls.objs:
            return cls.objs[cls]

        cls.objs_locker.acquire()
        try:
            if cls in cls.objs:  ## double check locking
                return cls.objs[cls]
            cls.objs[cls] = object.__new__(cls)
            return cls.objs[cls]
        finally:
            cls.objs_locker.release()

    def set_single_moive_data(self,movie_info):
        '''
        设置新的影片信息
        :param movie_info:
        :param arg:
        :return:
        '''
        movie_detail_objects = MovieModel.objects.filter(title=movie_info['title'])
        movie_objects  = MovieModel.objects.filter(title=movie_info['title'])

        if len(movie_detail_objects) > 0 or len(movie_objects):
            CSysLog.warn('data already existed')
            return
        else:
            new_movie = MovieModel()
            new_movie.title = movie_info['title']
            new_movie.release_time = movie_info['releaseTime']
            new_movie.major_img_url = movie_info['majorPicUrl']
            new_movie.moive_star_score = movie_info['starScore']
            new_movie.save()

            new_movie_detail = MovieModel()
            new_movie_detail.title=movie_info['title']
            new_movie_detail.release_time = movie_info['releaseTime']
            new_movie_detail.major_img_url = movie_info['majorPicUrl']
            new_movie_detail.moive_star_score = movie_info['starScore']
            new_movie_detail.content = movie_info['content']
            new_movie_detail.ftp_url = movie_info['ftpUrl']
            new_movie_detail.moive_detail = new_movie
            new_movie_detail.save()

    def set_array_movies_data(self,movie_info_array,data_type):
        '''
        传入数组影片信息进行保存数据库
        :param movie_info_array:影片详情列表,data_type:HomeData:0x01,LastestData:0x02,japan_korean_data:0x03,eur_amer_data:0x04
        :return:
        '''
        CSysLog.info('prepare to write data to database')
        if len(movie_info_array) < 1:
            return False

        if data_type == 0x00:
            home_movies_objects = MovieModel.objects.filter(movie_classify=data_type)
            if len(home_movies_objects) > 0:
                CSysLog.info('delete home data')
                home_movies_objects.delete()#首页数据更新需要先清空下原来的首页数据

        movie_objects = []
        for movie_info in movie_info_array:
            new_movie = MovieModel()
            CSysLog.info('before title %s'%(movie_info['title']))
            new_movie.title = movie_info['title']
            new_movie.release_time = movie_info['release_time']
            new_movie.major_img_url = movie_info['major_img_url']
            new_movie.moive_star_score = movie_info['movie_star_score']
            new_movie.moive_type = movie_info['movie_type']
            new_movie.movie_classify = movie_info['movie_classify']
            new_movie.movie_classify_child = movie_info['movie_classify_child']
            new_movie.summary_img_url = movie_info['summary_img_url']
            new_movie.content = movie_info['content']
            new_movie.ftp_url = movie_info['ftp_url']
            movie_objects.append(new_movie)

        MovieModel.objects.bulk_create(movie_objects)
        CSysLog.info('write data success')
        return True

    def update_data(self,movie_info):
        '''
        更新某项obd信息
        :param device_id:
        :param args:
        :return:
        '''


    def get_all_movies(self):
        '''
        获取所有影片
        :return:
        '''
        pass

    def get_movies_with_type(self,movie_type):
        '''
        根据影片类型获取相应的影片
        :param movie_type:
        :return:
        '''
        pass


    def get_intraday_mileage(self,device_id,timestamp):
        '''
        获取当日的油耗
        :param: device_id:目标OBD设备，timestamp:目标时间
        :return:当日的油耗
        '''
        dt_start_time,dt_end_time = self.parse_timestamp(timestamp)
        obd_info_objects = MovieModel.objects.filter(upload_time__range=(dt_start_time, dt_end_time), equipment_id=device_id)
        if len(obd_info_objects) > 0:
            intraday_total_mileage = 0
            for obd_info_object in obd_info_objects:
                intraday_total_mileage += int(obd_info_object.distance_single)

            return intraday_total_mileage
        else:
            return -1

    def parse_timestamp(self,timestamp):
        '''

        :param timestamp:
        :return: 当日开始时间和结束时间
        '''
        date_time = CTimeHelper.timestampToDatetime(timestamp)
        start_date = datetime.datetime(date_time.year, date_time.month, date_time.day,0,0,0)
        end_date = datetime.datetime(date_time.year, date_time.month, date_time.day,23,59,59)
        return start_date,end_date

    def get_intraday_fuel_consumption(self,device_id,timestamp):
        '''
        获取当日的行驶距离
        :param: device_id:目标OBD设备，timestamp:目标时间,需要解析下时间
        :return:
        '''
        dt_start_time, dt_end_time = self.parse_timestamp(timestamp)
        obd_info_objects = MovieModel.objects.filter(upload_time__range=(dt_start_time, dt_end_time), equipment_id=device_id)
        if len(obd_info_objects) > 0:
            intraday_total_fuel_consumption = 0
            for obd_info_object in obd_info_objects:
                intraday_total_fuel_consumption += int(obd_info_object.oiluse_single)

            return intraday_total_fuel_consumption
        else:
            return -1

    def get_intraday_fuel_and_mileage(self,device_id,timestamp):
        '''
        获取当日的行驶距离以及油耗
        :param device_id:目标OBD id
        :param timestamp:
        :return: 返回当日的油耗以及里程
        '''
        if type(timestamp) != int:
            CSysLog.error('timestamp type error not int')
            return None,None

        print 'get_intraday_fuel_and_mileage'

        dt_start_time, dt_end_time = self.parse_timestamp(timestamp)
        print dt_start_time,dt_end_time
        obd_info_objects = MovieModel.objects.filter(upload_time__range=(dt_start_time, dt_end_time), equipment_id=device_id)
        if len(obd_info_objects) > 0:
            intraday_total_fuel_consumption = 0
            intraday_total_mileage = 0
            for obd_info_object in obd_info_objects:
                intraday_total_fuel_consumption += int(obd_info_object.oiluse_single)
                intraday_total_mileage += int(obd_info_object.distance_single)
            return intraday_total_fuel_consumption, intraday_total_mileage
        else:
            return None,None

    def get_lastest_obd_info(self,device_id):
        '''
        获取最新的obd对应的信息
        :param device_id: 目标OBD
        :return: 最新的obd model对象
        '''
        obd_info_objects = MovieModel.objects.filter(equipment_id=device_id)
        if len(obd_info_objects) > 0:
            CSysLog.info('get obd inf objects :%d'%(len(obd_info_objects)))
            obd_object = obd_info_objects.order_by('upload_time')[0]
            CSysLog.info('distance_history :%s  drivetime_history: %s oiluse_history: %s'%(obd_object.distance_history,obd_object.drivetime_history,obd_object.oiluse_history))
            return obd_info_objects.order_by('upload_time')[0]
        else:
            CSysLog.warn('No obd_info object found yet')
            return None