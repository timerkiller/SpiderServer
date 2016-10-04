# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from app.models import MovieModel
from utilapp.tools import CMyTools
from app.database_operation.database_manager import DatabaseManager

def get_obd_info(request):
    if request.method == 'GET':
        if 'deviceId' in request.GET and 'timeStamp' in request.GET:
            deviceId = request.GET.get('deviceId').encode("utf-8")
            timeStamp = request.GET.get('timeStamp').encode("utf-8")
            print deviceId,timeStamp
            responseData = {
                'result':'ok',
                'intradayDrivingDistance':'', #当日行驶距离/m
                'intradayFuelConsumption':'', #当日行驶油耗/ml
                'historyTotalMileage':'',     #历史距离
                'historyTotalFuelConsumption':'',#历史油耗
                'historyDrivingTime':''         #历史家是时间
            }

            intradayFuelConsumption,intradayDrivingDistance = DatabaseManager.get_movie_model_instance().get_intraday_fuel_and_mileage(deviceId,int(timeStamp))
            lastObdInfo = DatabaseManager.get_movie_model_instance().get_lastest_obd_info(deviceId)
            if(lastObdInfo != None and intradayFuelConsumption != None and intradayDrivingDistance != None):
                responseData['intradayDrivingDistance']=str(intradayDrivingDistance)
                responseData['intradayFuelConsumption']=str(intradayFuelConsumption)
                responseData['historyTotalMileage']=lastObdInfo.distance_history
                responseData['historyTotalFuelConsumption']=lastObdInfo.oiluse_history
                responseData['historyDrivingTime']=lastObdInfo.drivetime_history

            else:
                responseData = {"result": "error", "errors": [{"errCode": 22, "desc": "未找到相关记录"}, ]}

            return HttpResponse(json.dumps(responseData), content_type='application/json')
        else:
            ret={"result":"error","errors":[{"errCode":4,"desc":"数据解析错误"},]}
            return HttpResponse(json.dumps(ret), content_type='application/json')
# Create your views here.
