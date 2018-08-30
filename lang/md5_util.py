# -*- coding: utf-8 -*-

import hashlib

'''
获取字符串的md5编码字符串
'''
def md5_encode(encoding_str):
    hash_md5 = hashlib.md5(encoding_str)
    return hash_md5.hexdigest()


'''
对文件进行md5编码
'''
def get_file_md5(file):
    m = hashlib.md5()

    while True:
        data = file.read(10240)
        if not data:
            break
        m.update(data)

    return m.hexdigest()
