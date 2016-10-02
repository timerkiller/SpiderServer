#coding=utf-8
from app.database_operation.movie_model_operation import MovieModelOperation
class DatabaseManager(object):

    @classmethod
    def get_example_model_instance(cls):
        '''
        获取相关model的操作接口
        :return:
        '''
        pass

    @classmethod
    def get_movie_model_instance(cls):
        '''
        获取OBD 模型的操作接口
        :return:
        '''
        instance = MovieModelOperation()
        return instance
