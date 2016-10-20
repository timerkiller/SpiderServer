#coding=utf-8
from app.models import MovieModel
from app.tool import Tool
from rest_api.error_code_list import CErrorCode
from loglib.logApi import CSysLog
from utilapp.page import CPageHelper,CPage
from utilapp.tools import CTimeHelper
class MovieManager(object):
    '''
    影片管理类，所有的影片获取接口都可以通过该接口获取
    '''

    class MovieClassType:
        HOME_PAGE = 0x00#主页数据
        NEW_MOV = 0x01#最新影片的数据
        EUR_US_MOV = 0x02  # 欧美电影数据
        JAP_KOR_MOV = 0x03#日韩电影数据
        CH_TELEPLAY = 0x04  # 国内电视剧
        VAIRETY_SHOW = 0x05  # 综艺
        US_TELEPLAY = 0x06  # 美剧
        STAR_SCORE = 0x07  # 评分最高
        CH_MOV = 0x08#国产电影

        GQDY = 0x100
        GQDY_NEWEST = 0x101
        GQDY_INDEX = 0x102

    class SortType:
        SORT_TIME = 0x00
        SORT_STAR_SCORE = 0x01
        SORT_POPULAR = 0x02

    @classmethod
    def list_item(cls,request):
        if 'movie_class_type' in request.data and 'sort_type' in request.data \
            and 'page_index' in request.data and 'per_page_size' in request.data:
            try:
                movie_class_type = int(request.data['movie_class_type'].encode('utf-8'))
                sort_type = int(request.data['sort_type'].encode('utf-8'))
                page_index = int(request.data['page_index'].encode('utf-8'))
                per_page_size = int(request.data['per_page_size'].encode('utf-8'))
                index_type_child = None
                if 'index_type_child' in request.data:
                    index_type_child = request.data['index_type_child'].encode('utf-8')

                return cls.parse_request_type(movie_class_type, sort_type, page_index, per_page_size,index_type_child)
            except Exception,e:
                CSysLog.info('parse movie type and sort type failed, reason:%s'%(e))
                return CErrorCode.DATA_PARSE_ERROR
        else:
            return CErrorCode.DATA_PARSE_ERROR


    @classmethod
    def search(cls,request):
        if 'condition' in request.data:
            condition = request.data['condition'].encode('utf-8')
            search_movie_objects = MovieModel.objects.filter(title__contains=condition).order_by('release_time')
            if len(search_movie_objects) > 0:
                resp_data = {'result': 'ok', 'movies': []}
                for movie in search_movie_objects:
                    page_container = {}
                    page_container['title'] = Tool.removeUnusefulText(movie.title)
                    page_container['star_score'] = str(movie.moive_star_score)
                    page_container['release_time'] = str(CTimeHelper.datetimeToInt(movie.release_time))
                    page_container['major_img_url'] = Tool.reMatchUrl(movie.major_img_url)
                    page_container['download_url'] = movie.ftp_url
                    page_container['content'] = movie.content
                    page_container['movie_type'] = movie.moive_type
                    page_container['summary_img_url'] = movie.summary_img_url
                    resp_data['movies'].append(page_container)
                return resp_data
            else:
                return CErrorCode.NO_EXPENSE_RECORD
        else:
            return CErrorCode.DATA_PARSE_ERROR


    @classmethod
    def parse_request_type(cls, movie_type, sort_type, page_index, per_page_size,index_type_child):
        if movie_type < cls.MovieClassType.HOME_PAGE or movie_type > cls.MovieClassType.CH_MOV \
                or sort_type < cls.SortType.SORT_TIME or sort_type > cls.SortType.SORT_POPULAR:
            return CErrorCode.TYPE_NOT_RESPONSE

        return cls.get_movie_list(movie_type,sort_type,page_index,per_page_size,index_type_child)

    @classmethod
    def get_movie_list(cls, movie_class_type, sort_type, page_index, per_page_size, index_type_child):
        movie_sort_type = cls.get_sort_type(sort_type)
        movie_objects = None
        if movie_class_type == cls.MovieClassType.HOME_PAGE and index_type_child != None:
            CSysLog.info('get home data and index_type_child :%s',index_type_child)
            movie_objects = MovieModel.objects.filter(movie_classify=movie_class_type|cls.MovieClassType.GQDY_NEWEST, movie_classify_child=index_type_child).order_by(movie_sort_type)
        else:
            movie_objects = MovieModel.objects.filter(movie_classify=movie_class_type).order_by("-" + movie_sort_type)
        if len(movie_objects) > 0:
            CSysLog.info("movie_object size :%d"%(len(movie_objects)))
            # page = CPage(movie_objects, per_page_size)
            # page_size = page.getPageCounts()
            # page_data = page.getPageDate(page_index)
            page_data,page_size = CPageHelper.pagination_display(movie_objects,page_index,per_page_size)
            resp_data = {'result': 'ok', 'total_page': str(page_size), 'movie_class_type':str(movie_class_type), 'movies': []}
            if page_index > page_size:
                return resp_data

            for page in page_data:
                page_container = {}
                page_container['id'] = page.id
                page_container['title'] = Tool.removeUnusefulText(page.title)
                page_container['star_score'] = str(page.moive_star_score)
                page_container['release_time'] = str(CTimeHelper.datetimeToInt(page.release_time))
                page_container['major_img_url'] = Tool.reMatchUrl(page.major_img_url)
                page_container['download_url'] = page.ftp_url
                page_container['content'] = page.content
                page_container['movie_type'] = page.moive_type
                page_container['summary_img_url'] = page.summary_img_url
                page_container['actor'] = page.actor
                page_container['country'] = page.country
                page_container['movie_source']=page.movie_source
                page_container['update_time']=page.update_time
                resp_data['movies'].append(page_container)
            return resp_data
        else:
            return CErrorCode.NO_EXPENSE_RECORD

    @classmethod
    def get_sort_type(cls,type):
        if type == cls.SortType.SORT_TIME:
            return 'release_time'
        elif type == cls.SortType.SORT_POPULAR:
            return 'popular'
        elif type == cls.SortType.SORT_STAR_SCORE:
            return '-moive_star_score'
