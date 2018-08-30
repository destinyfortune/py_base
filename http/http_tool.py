# coding: utf-8 -*-
# http工具类

import urllib
import urllib2
import requests


# urllib2
class UrlLib2(object):
    @staticmethod
    def get(url, timeout=None):
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req, timeout=timeout)
        return res_data.read()

    @staticmethod
    def post(url, params=None, timeout=None, need_encode=False):
        if need_encode:
            params = urllib.urlencode(params)
        req = urllib2.Request(url=url, data=params)
        res_data = urllib2.urlopen(req, timeout=timeout)
        return res_data.read()


class Requests(object):

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, timeout=10):
        resp = self.session.get(url, timeout=timeout)
        return resp

    def post(self, url, params=None, timeout=10, content_type=None):
        headers = {
            'Content-Type': content_type
        }
        resp = self.session.post(url, data=params, headers=headers, timeout=timeout)
        return resp.content