# -*- coding: utf-8 -*-
# 时间工具类
import time
import datetime


class date(object):

    """
    时间戳转日期
    """
    @classmethod
    def timestamp_to_date(cls, source, format='%Y-%m-%d %H:%M:%S'):
        time_array = time.localtime(float(source))
        target = time.strftime(format, time_array)
        return target

    """
    UTC时间转当前时间
    """
    @classmethod
    def utc_to_local(cls, utc_dt):
        now_stamp = time.time()
        local_date = datetime.datetime.fromtimestamp(now_stamp)
        utc_date = datetime.datetime.utcfromtimestamp(now_stamp)
        offset = local_date - utc_date
        target_local_date = utc_dt + offset
        return target_local_date


