import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
sys.path.append('.')
from databases.dbhelpers import *
from datamodels.crms.qlt_params import *
from datamodels.crms.qlt_thongtins import *
from utils.objecthelpers import helper
from utils.constants import *
import logging
logger = logging.getLogger(__name__)


class crmsdb:
    def __init__(self):
        self.db = oracledb()
        logger.info("====================================")
        logger.info("====================================")
        logger.info("Database connected")



#Get ID_PHIENBAN, ID_LYDOXEPHANG:
    def get_next_id_phienban(self):
        _id_phienban = 0
        try:

            logger.info("Bắt đầu - lấy thông tin SP_PhienBan_GetNextID")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_PhienBan_GetNextID")
            _id_phienban = result["data"][0][0]

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("Kết thúc - lấy thông tin SP_PhienBan_GetNextID")

        return _id_phienban

    #get id phien ban current: phục vụ tính điểm lại
    def get_current_id_phienban(self):
        _id_phienban = 0
        try:

            logger.info("Bắt đầu - lấy thông tin SP_PhienBan_GetCurrentID")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_PhienBan_GetCurrentID")
            _id_phienban = result["data"][0][0]

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("Kết thúc - lấy thông tin SP_PhienBan_GetCurrentID")

        return _id_phienban

    def get_next_id_lydoxephang(self):
        _id_lydo = 0
        try:
            logger.info("Bắt đầu - lấy thông tin SP_LyDoXH_GetID")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_LyDoXH_GetID")
            _id_lydo = result["data"][0][0]

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("Kết thúc - lấy thông tin SP_LyDoXH_GetID")

        return _id_lydo



    def get_XHDN_TH_GetID(self):
        _id = 0
        try:
            logger.info("Bắt đầu - lấy thông tin SP_XHDN_TH_GetID")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_XHDN_TH_GetID")
            _id = result["data"][0][0]

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("Kết thúc - lấy thông tin SP_XHDN_TH_GetID")

        return _id

    def XHDN_TH_Update(self, id):
        try:
            logger.info("Bắt đầu - Update thông tin XHDN_TH_Update")
            self.db.execprocnoquery("CRMS.PKG_XHDN_V2.SP_XHDN_TH_Update", p_ID = id)
        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("Kết thúc - Update thông tin XHDN_TH_Update")

# Insert thông tin QLT_TMP_XEPHANGDN_20 (:ID_PHIENBAN,:MADN,:DIEMPHANLOAINK,:DIEMPHANLOAIXK,:HANGNK,:HANGXK, :ID_LYDOXEPHANG)
    def insert_qlt_tmp_xephangdn(self, datas):
        try:
            logger.info("Bắt đầu - Insert thông tin QLT_TMP_XEPHANGDN_20 BATCH_SIZE: {}".format(const_crms.BATCH_SIZE))
            _sqltext = "insert into QLT_TMP_XEPHANGDN_20 values(:1,:2,:3,:4,:5,:6,:7)"
            self.db.execnonquerybatch(_sqltext, datas, const_crms.BATCH_SIZE)
        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - Insert thông tin QLT_XEPHANGDN_20")

    def insert_qlt_xephangdn(self, _ID_PHIENBAN, _ID_LYDOXEPHANG):
        try:
            logger.info("Bắt đầu - Insert thông tin QLT_XEPHANGDN_20 ")
            self.db.execprocnoquerytrans("CRMS.PKG_XHDN_V2.QLT_XepHangDN_Insert", p_id_phienban =_ID_PHIENBAN , p_id_lydoxephang =_ID_LYDOXEPHANG)
        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - Insert thông tin QLT_XEPHANGDN_20")

# Insert lý do xếp hạng điểm hsdn:
# Insert thông tin QLT_LYDOXEPHANG_HSDN_DIEMTC_20 (:ID_PHIENBAN,:MADN,:NK_XK,:ID_TIEUCHI,:DIEM,:DIEMPHAT)
    def insert_hsdn_lydoxephang_diemtc(self, datas):
        try:
            logger.info("Bắt đầu - Insert thông tin QLT_LYDOXEPHANG_HSDN_DIEMTC_20 BATCH_SIZE: {}".format(const_crms.BATCH_SIZE))
            _sqltext = "insert into QLT_LYDOXEPHANG_HSDN_DIEMTC_20 values(:1,:2,:3,:4,:5,:6)"
            self.db.execnonquerybatch(_sqltext, datas, const_crms.BATCH_SIZE)
        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - Insert thông tin QLT_LYDOXEPHANG_HSDN_DIEMTC_20")


#get thông tin params SP_GET_QLT_PARAMS_PLXEPHANG
    def get_params_plxephangs(self):
        try:
            logger.info("Bắt đầu - lấy thông tin QLT_PARAMS_PLXEPHANG")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_PLXEPHANG")
            cols = result["col"]
            datas = result["data"]
            lstplxephangs = []  # khởi tạo một list QLT_PARAMS_PLXEPHANG
            for row in datas:
                kl = QLT_PARAMS_PLXEPHANG()
                helper.toObject(cols, row, kl)
                lstplxephangs.append(kl)

            return lstplxephangs

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - lấy thông tin QLT_PARAMS_PLXEPHANG")

#get thông tin doanh nghiệp
    def get_hsdns(self,FromRowID: int, ToRowID: int, IsTinhLai: int):
        try:
            logger.info("Bắt đầu - lấy thông tin QLT_THONGTINDOANHNGHIEP")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_THONGTINDOANHNGHIEP",p_FromRowID = FromRowID, p_ToRowID = ToRowID, p_IsTinhLai = IsTinhLai)
            cols = result["col"]
            datas = result["data"]
            lstHSDNs = []  # khởi tạo một list QLT_THONGTINDOANHNGHIEP
            for row in datas:
                objHSDN = QLT_THONGTINDOANHNGHIEP()
                helper.toObject(cols, row, objHSDN)
                lstHSDNs.append(objHSDN)

            return lstHSDNs

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - lấy thông tin QLT_THONGTINDOANHNGHIEP")

    def get_hsdn_params(self):
        try:
            logger.info("Bắt đầu - lấy thông tin các bảng params HSDN")
            hsdn_params = {}
            #1. QLT_PARAMS_HSDN_TC_MOTA
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSDN_TC_MOTA")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSDN_TC_MOTA
            #objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSDN_TC_MOTA()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_TC_MOTA] = lstPARAMS
            #END QLT_PARAMS_HSDN_TC_MOTA

            #2. QLT_PARAMS_HSDN_DGTC
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSDN_DGTC")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSDN_DGTC
            #objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSDN_DGTC()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_DGTC] = lstPARAMS
            # END QLT_PARAMS_HSDN_DGTC

            #3. QLT_PARAMS_HSDN_PLDCC
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSDN_PLDCC")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSDN_PLDCC
            #objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSDN_PLDCC()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_PLDCC] = lstPARAMS
            # END QLT_PARAMS_HSDN_PLDCC

            # 4. QLT_PARAMS_HSDN_PTAD
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSDN_PTAD")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSDN_PTAD
            #objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSDN_PTAD()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_PTAD] = lstPARAMS
            # END QLT_PARAMS_HSDN_PLDCC

            # 5. lấy MIN ID, MAX ID QLT_THONGTINDOANHNGHIEP
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GetMinMaxID")
            cols = result["col"]
            datas = result["data"]
            hsdn_params[const_hsdn_params.QLT_MIN_MAX_ID] = (datas[0][cols["ROW_MIN_ID"]], datas[0][cols["ROW_MAX_ID"]])
            # END lấy MIN ID, MAX ID QLT_THONGTINDOANHNGHIEP

            return hsdn_params
        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - lấy thông tin các bảng params HSDN")

#END get thông tin doanh nghiệp

# get  thông tin vi phạm
    def get_hsvps(self):
        try:
            logger.info("Bắt đầu - lấy thông tin QLT_THONGTINVIPHAM")
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_THONGTINVIPHAM")
            cols = result["col"]
            datas = result["data"]
            lstHSVPs = []  # khởi tạo một list QLT_THONGTINVIPHAM
            objHVP = None
            for row in datas:
                objHVP = QLT_THONGTINVIPHAM()
                helper.toObject(cols, row, objHVP)
                lstHSVPs.append(objHVP)

            return lstHSVPs

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - lấy thông tin QLT_THONGTINVIPHAM")

    def get_hsvp_params(self):
        try:
            logger.info("Bắt đầu - lấy thông tin các bảng params HSVP")
            hsvp_params = {}
            # 1. QLT_PARAMS_HSVP_HSPLTN
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_HSPLTN")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_HSPLTN
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_HSPLTN()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_HSPLTN] = lstPARAMS
            # END QLT_PARAMS_HSVP_HSPLTN

            # 2. QLT_PARAMS_HSVP_HSPLXNK
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_HSPLXNK")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_HSPLXNK
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_HSPLXNK()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_HSPLXNK] = lstPARAMS
            # END QLT_PARAMS_HSVP_HSPLXNK

            # 3. QLT_PARAMS_HSVP_PLCLT
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_PLCLT")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_PLCLT
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_PLCLT()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLCLT] = lstPARAMS
            # END QLT_PARAMS_HSVP_PLCLT

            # 4. QLT_PARAMS_HSVP_PLHSVP
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_PLHSVP")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_PLHSVP
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_PLHSVP()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLHSVP] = lstPARAMS
            # END QLT_PARAMS_HSVP_PLHSVP

            # 5. QLT_PARAMS_HSVP_PLSLVP
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_PLSLVP")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_PLSLVP
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_PLSLVP()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLSLVP] = lstPARAMS
            # END QLT_PARAMS_HSVP_PLSLVP

            # 6. QLT_PARAMS_HSVP_PLTLVP
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_PLTLVP")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_PLTLVP
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_PLTLVP()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLTLVP] = lstPARAMS
            # END QLT_PARAMS_HSVP_PLTLVP

            # 7. QLT_PARAMS_HSVP_PLVP
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_PLVP")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_PLVP
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_PLVP()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVP] = lstPARAMS
            # END QLT_PARAMS_HSVP_PLVP

            # 8. QLT_PARAMS_HSVP_PLVPKTK
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_PARAMS_HSVP_PLVPKTK")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_PARAMS_HSVP_PLVPKTK
            objParam = None
            for row in datas:
                objParam = QLT_PARAMS_HSVP_PLVPKTK()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVPKTK] = lstPARAMS
            # END QLT_PARAMS_HSVP_PLVPKTK

            # 9. QLT_HSVP_SOTOKHAIDUOCTHONGQUAN
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_QLT_SOTK_THONGQUAN")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_HSVP_SOTOKHAIDUOCTHONGQUAN
            objParam = None
            for row in datas:
                objParam = QLT_HSVP_SOTOKHAIDUOCTHONGQUAN()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_HSVP_SOTOKHAIDUOCTHONGQUAN] = lstPARAMS
            # END QLT_HSVP_SOTOKHAIDUOCTHONGQUAN

            # 10. QLT_HSVP_VIPHAMTOKHAI
            result = self.db.execproc("CRMS.PKG_XHDN_V2.SP_GET_VIPHAMTOKHAI")
            cols = result["col"]
            datas = result["data"]
            lstPARAMS = []  # khởi tạo một list QLT_HSVP_VIPHAMTOKHAI
            objParam = None
            for row in datas:
                objParam = QLT_HSVP_VIPHAMTOKHAI()
                helper.toObject(cols, row, objParam)
                lstPARAMS.append(objParam)

            hsvp_params[const_hsvp_params.QLT_HSVP_VIPHAMTOKHAI] = lstPARAMS
            # END QLT_HSVP_VIPHAMTOKHAI

            return hsvp_params
        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("kết thúc - lấy thông tin các bảng params HSVP")



## test get data
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
## end test get data
