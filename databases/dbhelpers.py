import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
sys.path.append('.')

import cx_Oracle
from configs.configsettings import *
from utils.loghelper import Logger

import logging
logger = logging.getLogger(__name__)


## function thực hiện lấy ra dictionary row name : rowindex của cursor
def fields(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1

    return results

##class phục vụ connect database oracle
class oracledb:
    def __init__(self):
        self.hostname = oracleconfig.hostname
        self.username = oracleconfig.username
        self.password = oracleconfig.password
        self.conn = None
        self.cur = None
        #self.logger = Logger(self.__class__.__name__).get() 

    def __connect__(self):
        self.conn = cx_Oracle.connect(self.username, self.password, self.hostname)
        self.cur = self.conn.cursor()

    def __disconnect__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

## excecute using sqlquery binding:
    def execquery(self,sql,**params):
        self.__connect__()
        self.cur.execute(sql,keywordParameters=params)
        cols = fields(self.cur)
        data=self.cur.fetchall() # đoạn này có thể thay bằng fetchmany(batch_size)
        self.__disconnect__()
        result = {"col" : cols, "data" : data}
        return result

    def execquerybatch(self,sql, batch_size, **params):
        self.__connect__()
        self.cur.execute(sql,keywordParameters=params)
        cols = fields(self.cur)
        data=self.cur.fetchmany(batch_size) # đoạn này có thể thay bằng fetchmany(batch_size)
        self.__disconnect__()
        result = {"col" : cols, "data" : data}
        return result

    def execnonquery(self, sql,**params):
        self.__connect__()
        self.cur.execute(sql,keywordParameters=params)
        self.__disconnect__()

    def exectrans(self, sql,**params):
        try:
            self.__connect__()
            self.conn.begin()
            self.cur.execute(sql,keywordParameters=params)
            self.conn.commit()
        except cx_Oracle.Error as ex:
            self.conn.rollback()
        finally:
            self.__disconnect__()

    ## thực hiện batch sql ( DML một lô dữ liệu (datas truyền vào là một list của tuple))
    ## datas = [(a,b,c), (b,c,d), ... (...)]
    ## sql truyền vào dạng : insert into values(:1,:2,:3) tùy thuộc độ dài của tuple
    def execnonquerybatch(self, sql,datas,batch_size: int):
        try:
            self.__connect__()
            self.conn.begin()
            databatchs = []
            for data in datas:
                databatchs.append(data)
                if len(databatchs) % batch_size ==0:
                    self.cur.executemany(sql,databatchs)
                    databatchs = []
            if databatchs:    
                self.cur.executemany(sql,databatchs)
                
            self.conn.commit()
        except cx_Oracle.Error as ex:
            self.conn.rollback()
        finally:
            self.__disconnect__()

## excecute using procedure or package
    def execproc(self,procname,**params):
        #print(params)
        self.__connect__()
        pref_cursor = self.conn.cursor()
        params['pref_cursor'] = pref_cursor
        #print(params)
        #Cursor.callfunc(name, returnType, parameters=[], keywordParameters = {})
        self.cur.callproc(procname,keywordParameters=params)
        cols = fields(pref_cursor)
        data = pref_cursor.fetchall() # đoạn này có thể thay bằng fetchmany(batch_size)
        self.__disconnect__()
        result = {"col" : cols, "data" : data}
        return result

    def execprocbatch(self,procname,batch_size,**params):
        #print(params)
        self.__connect__()
        pref_cursor = self.conn.cursor()
        params['pref_cursor'] = pref_cursor
        #print(params)
        #Cursor.callfunc(name, returnType, parameters=[], keywordParameters = {})
        self.cur.callproc(procname,keywordParameters=params)
        cols = fields(pref_cursor)
        data = pref_cursor.fetchmany(batch_size) # đoạn này có thể thay bằng fetchmany(batch_size)
        self.__disconnect__()
        result = {"col" : cols, "data" : data}
        return result

    def execprocnoquery(self,procname,**params):
        self.__connect__()
        self.cur.callproc(procname,keywordParameters=params)
        self.__disconnect__()

    def execprocnoquerytrans(self,procname,**params):
        try:
            self.__connect__()
            self.conn.begin()
            self.cur.callproc(procname,keywordParameters=params)
            self.conn.commit()
        except cx_Oracle.Error as ex:
            self.conn.rollback()
            print(ex)
        finally:
            self.__disconnect__()

