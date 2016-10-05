from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response as rest_response
from error_code_list import CErrorCode
from loglib.logApi import CSysLog
# Create your views here.
from manager.movie_manager import MovieManager

@api_view(['POST'])
def movie(request):
    CSysLog.info(request.data)
    if 'mode' in request.data:
        mode = request.data['mode'].encode('utf-8')
        if mode == 'list':
            result = MovieManager.list_item(request)
            return rest_response(result)
        elif mode == 'search':
            result = MovieManager.search(request)
            return rest_response(result)
        else:
            return rest_response(CErrorCode.DATA_PARSE_ERROR)
    else:
        return rest_response(CErrorCode.SYNTAX_ERROR)


@api_view(['POST'])
def user(request):
    return rest_response(CErrorCode.DATA_PARSE_ERROR)

@api_view(['POST'])
def auth(request):
    return rest_response(CErrorCode.DATA_PARSE_ERROR)