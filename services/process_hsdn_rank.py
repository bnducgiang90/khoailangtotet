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
    def __init__(self, _lstHSDNs : [], _params_hsdn : {}):
        #self._srvcrms = crmsservice()
        self._hsdn_params = _params_hsdn
        self._HSDNs = _lstHSDNs
        #self.qlt_hsdn_xhdns : List[qlt_hsdn_xhdn] = []

    # thực hiện tính điểm, điểm phạt, điểm max của danh sách doanh nghiệp theo tiêu chí

    def process_qlt_hsdn_xhdn(self):
        _qlt_hsdn_xhdns: List[qlt_hsdn_xhdn] = []

        for qlt_ttdn in self._HSDNs:
            lstKLs = []

            for param in self._hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_TC_MOTA]:
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

            objqlt_hsdn_xhdn = qlt_hsdn_xhdn(qlt_ttdn.MA_DN, lstKLs,  self._hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_PLDCC])
            _qlt_hsdn_xhdns.append(objqlt_hsdn_xhdn)

        return _qlt_hsdn_xhdns

    # thực hiện tính điểm, điểm phạt, điểm max của từng tiêu chí
    def set_diem_tieuchi_hsdn(self, kl: qlt_tieuchi_hsdn):
        try:
            _params_hsdn_dgtc: List[QLT_PARAMS_HSDN_DGTC] = [item for item in
                                                            self._hsdn_params[const_hsdn_params.QLT_PARAMS_HSDN_DGTC]
                                                            if item.ID_TIEUCHI == kl.ID_TIEUCHI
                                                           ]
            ## sắp xếp lại theo giá trị của tiêu chí:
            _params_hsdn_dgtc.sort(key = lambda item: item.GIATRI, reverse=False)

            if kl.PHUONGTHUCAPDUNG == const_crms.PTAD_MA:
                if kl.GIA_TRI == _params_hsdn_dgtc[0].GIATRI:
                    kl.DIEM = _params_hsdn_dgtc[0].DIEMSO
                    kl.DIEMPHAT = _params_hsdn_dgtc[0].DIEMPHAT
            else:
                for item in _params_hsdn_dgtc:
                    if kl.GIA_TRI <= item.GIATRI:
                        kl.DIEM = item.DIEMSO
                        kl.DIEMPHAT = item.DIEMPHAT
                        break
            if kl.DIEM is None or kl.DIEMPHAT is None:
                logger.warning("ID_TIEUCHI : {} có giá trị {} không phù hợp với bảng tham số có giá trị MAX là {} "
                               .format(kl.ID_TIEUCHI, kl.GIA_TRI,
                                       _params_hsdn_dgtc[-1].GIATRI)
                               )
            else :
                kl.DIEM_MAX = max(item.DIEMSO for item in _params_hsdn_dgtc)

        except Exception as ex:
            logger.exception("Lỗi Giá trị {} ID_TIEUCHI : {}".format( kl.GIA_TRI, kl.ID_TIEUCHI))

