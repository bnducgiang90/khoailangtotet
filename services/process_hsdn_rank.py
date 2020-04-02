import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)
from typing import List

from services.crmsservices import *
from utils.constants import *
from datamodels.crms.qlt_hsdn_xhdn import  *
from datamodels.crms.qlt_params import *

class process_rank_hsdn:
    def __init__(self, lstHSDNs : [], params_hsdn : {}):
        self.srvcrms = crmsservice()
        self.hsdn_params = params_hsdn
        self.HSDNs = lstHSDNs
        #self.qlt_hsdn_xhdns : List[qlt_hsdn_xhdn] = []

    # thực hiện tính điểm, điểm phạt, điểm max của danh sách doanh nghiệp theo tiêu chí
    @property
    def get_qlt_hsdn_xhdns(self):
        _qlt_hsdn_xhdns: List[qlt_hsdn_xhdn] = []

        for qlt_ttdn in self.HSDNs:
            lstKLs = []

            for param in self.hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_TC_MOTA]:
                kl = qlt_tieuchi_hsdn()
                kl.MA_DN = qlt_ttdn.MA_DN
                kl.ID_TIEUCHI = param.ID_TIEUCHI
                kl.ID_NHOM = param.ID_NHOM
                kl.NK_XK = param.NK_XK
                kl.PHUONGTHUCAPDUNG = param.PHUONGTHUCAPDUNG

                if hasattr(qlt_ttdn, param.COLUMNNAME) :
                    kl.GIA_TRI = getattr(qlt_ttdn,param.COLUMNNAME)
                elif hasattr(qlt_ttdn, param.COLUMNNAME.upper()) :
                    kl.GIA_TRI = getattr(qlt_ttdn, param.COLUMNNAME.upper())
                else:
                    logger.warning("QLT_THONGTINDOANHNGHIEP không có attr {}".format(param.COLUMNNAME))

                self.set_diem_tieuchi_hsdn(kl)
                lstKLs.append(kl)

            objqlt_hsdn_xhdn = qlt_hsdn_xhdn(qlt_ttdn.MA_DN, lstKLs,  self.hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_PLDCC])
            _qlt_hsdn_xhdns.append(objqlt_hsdn_xhdn)

        return _qlt_hsdn_xhdns

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

