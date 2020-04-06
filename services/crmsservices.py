import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
from typing import List

from datamodels.crms.qlt_xhdn import QLT_XEPHANGDN_20, QLT_LYDOXEPHANG_HSDN_DIEMTC

sys.path.append('.')
# define top level module logger
import logging
logger = logging.getLogger(__name__)

from databases.crmsdb import *


class crmsservice:
    def __init__(self):
        self.db = crmsdb()

# Get ID_PHIENBAN, ID_LYDOXEPHANG:
    def get_id_phienban(self, istinhlai):
        _id_phienban = self.db.get_next_id_phienban()
        if istinhlai == const_crms.IS_TINHLAI:
            _id_phienban = self.db.get_current_id_phienban()
        return _id_phienban

    def get_next_id_lydoxephang(self):
        _id_lydo = self.db.get_next_id_lydoxephang()
        return _id_lydo

    def get_XHDN_TH_GetID(self):
        _id = self.db.get_XHDN_TH_GetID()
        return _id

    def XHDN_TH_Update(self, id):
        self.db.XHDN_TH_Update(id)

#insert_qlt_xephangdn
    def insert_qlt_tmp_xephangdn(self, datas: []):
        _qlt_xephangs:List[QLT_XEPHANGDN_20] = datas
        _tuple_params = [(item.ID_PHIENBAN, item.MADN, item.DIEMPHANLOAINK, item.DIEMPHANLOAIXK, item.HANGNK, item.HANGXK, item.ID_LYDOXEPHANG)
                         for item in _qlt_xephangs
                        ]
        self.db.insert_qlt_tmp_xephangdn(_tuple_params)

    def insert_qlt_xephangdn(self, _ID_PHIENBAN, _ID_LYDOXEPHANG):
        self.db.insert_qlt_xephangdn(_ID_PHIENBAN, _ID_LYDOXEPHANG)

# insert_hsdn_lydoxephang_diemtc
    def insert_hsdn_lydoxephang_diemtc(self, datas):
        _lst_lydo_diem_tc: List[QLT_LYDOXEPHANG_HSDN_DIEMTC] = datas
        _tuple_params = [(item.ID_PHIENBAN, item.MADN, item.NK_XK, item.ID_TIEUCHI, item.DIEM,
                          item.DIEMPHAT)
                         for item in _lst_lydo_diem_tc
                         ]

        self.db.insert_hsdn_lydoxephang_diemtc(_tuple_params)

## QLT_PARAMS_PLXEPHANG:
    def get_params_plxephangs(self):
        _plxephangs = self.db.get_params_plxephangs()
        return _plxephangs

##get thông tin doanh nghiệp
    def get_hsdns(self,FromRowID: int, ToRowID: int, IsTinhLai: int) -> []:
        lstHSDNs = self.db.get_hsdns(FromRowID, ToRowID, IsTinhLai)
        return lstHSDNs

    def get_hsdn_params(self) -> {}:
        hsdn_params = self.db.get_hsdn_params()
        return hsdn_params

##END get thông tin doanh nghiệp

##get thông tin hồ sơ vi phạm
    def get_hsvps(self) -> []:
        lstHSVPs = self.db.get_hsvps()
        return lstHSVPs

    def get_hsvp_params(self) -> {}:
        hsvp_params = self.db.get_hsvp_params()
        return hsvp_params

##END get thông tin doanh nghiệp



#test:
    def getdata(self) -> []:
        lstobj = self.db.getdata()
        return lstobj
#END test

