import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
sys.path.append('.')
from databases.dbhelpers import *
from datamodels.crms.xephangdoanhnghiep import *
from utils.objecthelpers import helper
import logging
logger = logging.getLogger(__name__)


class crmsdatabase:
    def __init__(self):
        self.db = oracledb()
        logger.info("Database connected")

    def getdata(self):
        try:
            logger.info("Bắt đầu getdata")
            results = self.db.execquery(
                'select ID,MA_DV from CRMS_TOKHAI_NOTHUE WHERE ROWNUM<5')
            cols = results["col"]
            datas = results["data"]
            # print(datas)
            listobj = []  # khởi tạo một list nợ thuế
            obj = None
            for row in datas:
                obj = crms_tokhai_nothue()
                # for key in cols.keys():
                #    if hasattr(obj,key):
                #        print("key {} : value : {}".format(key,row[cols[key]]))
                #        setattr(obj,key,row[cols[key]])
                helper.toObject(cols, row, obj)
                listobj.append(obj)

            return listobj

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc : getdata!")

    def getdata_proc(self, id: int):
        try:
            logger.info("Bắt đầu getdata_proc")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GETDATA", pID=None)
            cols = result["col"]
            datas = result["data"]
            listobj = []  # khởi tạo một list nợ thuế
            obj = None
            for row in datas:
                obj = crms_tokhai_nothue()
                helper.toObject(cols, row, obj)
                listobj.append(obj)

            return listobj

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc : getdata_proc id = {}".format(id))
