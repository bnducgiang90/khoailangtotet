import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)
from typing import List

from services.crmsservices import *
from utils.constants import *
from datamodels.crms.qlt_tieuchi_hsdn import  *

class process_rank_hsdn:
    def __init__(self, lstHSDNs : [], params_hsdn : {}):
        self.srvcrms = crmsservice()
        self.hsdn_params = params_hsdn
        self.HSDNs = lstHSDNs
        self.qlt_hsdn_xhdns : List[qlt_hsdn_xhdn] = []

    def get_qlt_hsdn_xhdns(self):

        for qlt_ttdn in self.HSDNs:
            lstqlt_tieuchi_hsdns = []

            for param in self.hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_TC_MOTA]:
                objqlt_tieuchi_hsdn = qlt_tieuchi_hsdn()
                objqlt_tieuchi_hsdn.MA_DN = qlt_ttdn.MA_DN
                objqlt_tieuchi_hsdn.ID_TIEUCHI = param.ID_TIEUCHI
                objqlt_tieuchi_hsdn.ID_NHOM = param.ID_NHOM
                objqlt_tieuchi_hsdn.NK_XK = param.NK_XK
                objqlt_tieuchi_hsdn.PHUONGTHUCAPDUNG = param.PHUONGTHUCAPDUNG

                if hasattr(qlt_ttdn, param.COLUMNNAME) :
                    objqlt_tieuchi_hsdn.GIA_TRI = getattr(qlt_ttdn,param.COLUMNNAME)
                elif hasattr(qlt_ttdn, param.COLUMNNAME.upper()) :
                    objqlt_tieuchi_hsdn.GIA_TRI = getattr(qlt_ttdn, param.COLUMNNAME.upper())
                else:
                    logger.warning("QLT_THONGTINDOANHNGHIEP không có attr {}".format(param.COLUMNNAME))

                self.set_diem_tieuchi_hsdn(objqlt_tieuchi_hsdn)
                lstqlt_tieuchi_hsdns.append(objqlt_tieuchi_hsdn)

            objqlt_hsdn_xhdn = qlt_hsdn_xhdn(qlt_ttdn.MA_DN, lstqlt_tieuchi_hsdns)
            self.qlt_hsdn_xhdns.append(objqlt_hsdn_xhdn)

        return self.qlt_hsdn_xhdns

    def tinh_giatri_diem_tieuchi_hsdn(self):
        tieuchi_hsdns = {}
        for qlt_ttdn in self.HSDNs:
            lstqlt_tieuchi_hsdns = []

            for param in self.hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_TC_MOTA]:
                objqlt_tieuchi_hsdn = qlt_tieuchi_hsdn()
                objqlt_tieuchi_hsdn.MA_DN = qlt_ttdn.MA_DN
                objqlt_tieuchi_hsdn.ID_TIEUCHI = param.ID_TIEUCHI
                objqlt_tieuchi_hsdn.ID_NHOM = param.ID_NHOM
                objqlt_tieuchi_hsdn.NK_XK = param.NK_XK
                objqlt_tieuchi_hsdn.PHUONGTHUCAPDUNG = param.PHUONGTHUCAPDUNG

                if hasattr(qlt_ttdn, param.COLUMNNAME) :
                    objqlt_tieuchi_hsdn.GIA_TRI = getattr(qlt_ttdn,param.COLUMNNAME)
                elif hasattr(qlt_ttdn, param.COLUMNNAME.upper()) :
                    objqlt_tieuchi_hsdn.GIA_TRI = getattr(qlt_ttdn, param.COLUMNNAME.upper())
                else:
                    logger.warning("QLT_THONGTINDOANHNGHIEP không attr {}".format(param.COLUMNNAME))
                self.set_diem_tieuchi_hsdn(objqlt_tieuchi_hsdn)
                lstqlt_tieuchi_hsdns.append(objqlt_tieuchi_hsdn)

            tieuchi_hsdns[qlt_ttdn.MA_DN] = lstqlt_tieuchi_hsdns

        return tieuchi_hsdns

    # thực hiện tính điểm, điểm phạt, điểm max của từng tiêu chí
    def set_diem_tieuchi_hsdn(self, objqlt_tieuchi_hsdn: qlt_tieuchi_hsdn):
        try:
            params_hsdn_dgtc: List[QLT_PARAMS_HSDN_DGTC] = [item for item in
                                                            self.hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_DGTC]
                                                            if item.ID_TIEUCHI == objqlt_tieuchi_hsdn.ID_TIEUCHI
                                                            ]
            ## sắp xếp lại theo giá trị của tiêu chí:
            params_hsdn_dgtc.sort(key = lambda item: item.GIATRI, reverse=False)

            if objqlt_tieuchi_hsdn.PHUONGTHUCAPDUNG == const_crms.PTAD_MA:
                if objqlt_tieuchi_hsdn.GIA_TRI == params_hsdn_dgtc[0].GIATRI:
                    objqlt_tieuchi_hsdn.DIEM = params_hsdn_dgtc[0].DIEMSO
                    objqlt_tieuchi_hsdn.DIEMPHAT = params_hsdn_dgtc[0].DIEMPHAT
            else:
                for item in params_hsdn_dgtc:
                    if objqlt_tieuchi_hsdn.GIA_TRI <= item.GIATRI:
                        objqlt_tieuchi_hsdn.DIEM = item.DIEMSO
                        objqlt_tieuchi_hsdn.DIEMPHAT = item.DIEMPHAT
                        break
            if objqlt_tieuchi_hsdn.DIEM is None or objqlt_tieuchi_hsdn.DIEMPHAT is None:
                logger.warning("ID_TIEUCHI : {} có giá trị {} không phù hợp với bảng tham số có giá trị MAX là {} "
                               .format(objqlt_tieuchi_hsdn.ID_TIEUCHI, objqlt_tieuchi_hsdn.GIA_TRI,
                                       params_hsdn_dgtc[-1].GIATRI)
                               )
            else :
                objqlt_tieuchi_hsdn.DIEM_MAX = max(item.DIEMSO for item in params_hsdn_dgtc)

        except Exception as ex:
            logger.exception("Lỗi Giá trị {} ID_TIEUCHI : {}".format( objqlt_tieuchi_hsdn.GIA_TRI, objqlt_tieuchi_hsdn.ID_TIEUCHI))


    ## tính tổng điểm phân loại của nhóm
    def tinh_diemphanloai_nhomtieuchi(self):
        pass

    ## tính tỷ trọng phân loại của nhóm
    def tinh_tytrongphanloai_nhomtieuchi(self):
        pass

