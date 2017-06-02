#coding:utf8
from django.apps import AppConfig
import os

default_app_config = 'booksys.BookSysConfig'
VERBOSE_APP_NAME = u'图书推荐系统'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class BookSysConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME