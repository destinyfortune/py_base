# -*- coding: utf-8 -*-
# mysql连接工具类

import pymysql


class mysql_conn(object):
    '''
    初始化
    '''

    def __init__(self, host, user, passwd, database, charset='utf-8',
                 use_unicode=True):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.use_unicode = use_unicode
        try:
            self.conn = pymysql.connect(host=host, user=user, passwd=passwd,
                                        database=database)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except pymysql.Error, e:
            print('连接数据库失败', e)
            raise e

    def fetch_one(self, sql):
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            return row
        except pymysql.Error, e:
            raise e

    def fetch_all(self, sql):
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except pymysql.Error, e:
            print('查询数据库失败', e)

    def filter(self, table, **kwargs):
        try:
            _initial = "SELECT * FROM %s WHERE " % table
            _filter_condition = self._build_filter_condition('and ', **kwargs)
            sql = _initial + _filter_condition
            return self.fetch_all(sql)
        except pymysql.Error, e:
            self.conn.rollback()
            raise e

    def insert(self, table, **kwargs):
        result = None
        try:
            columns = kwargs.keys()
            _initial = "INSERT INTO %s" % table
            _fields = ",".join(["".join(['`', column, '`'])
                                for column in columns])
            _values = ",".join(["%s" for i in range(len(columns))])
            _sql = "".join([_initial, "(", _fields, ")VALUES(", _values, ")"])
            _param = [kwargs.get(column) for column in columns]
            result = self.cursor.execute(_sql, tuple(_param))
            self.conn.commit()
        except pymysql.Error, e:
            self.conn.rollback()
            raise e
        return result

    def update(self, table, condition, **kwargs):
        result = {}
        try:
            if len(kwargs) > 0:
                _initial = "UPDATE `%s` SET " % table
                _update_str = self._build_filter_condition(', ', **kwargs)
                _where_condition = self._build_filter_condition('and ', **condition)
                _sql = _initial + _update_str + ' WHERE ' + _where_condition
                result = self.cursor.execute(_sql)
                self.conn.commit()
        except pymysql.Error, e:
            self.conn.rollback()
            raise e
        return result

    '''
    查询数据库，若不存在即创建，存在即更新
    '''
    def get_or_create(self, table, where_obj, *args, **kwargs):
        records = self.filter(table, **where_obj)
        if records and len(records) > 0:
            record = records[0]
            update_dict = {}
            for k in kwargs.keys():
                if k in record:
                    if record[k] != kwargs.get(k):
                        update_dict[k] = kwargs.get(k)
            self.update(table, where_obj, **update_dict)
        else:
            self.insert(table, **kwargs)


    '''
    根据where条件构建where语句
    '''
    def _build_filter_condition(self, join_mark, **kwargs):
        _where_obj = []
        if kwargs:
            for k, v in kwargs.iteritems():
                if isinstance(v, int) or isinstance(v, float):
                    _where_obj.append("%s = %s " % (k, v))
                else:
                    _where_obj.append("%s = '%s' " % (k, v))
        return join_mark.join(_where_obj)


    '''
    delete操作慎用，暂时不往下写    
    '''
    def delete(self, table, condition):
        _initial = "".join(['DELETE FROM ', table, 'WHERE'])
        _sql = "".join([_initial, condition])
        return self.cursor.execute(_sql)

    def close(self):
        self.conn.close()
        self.cursor.close()