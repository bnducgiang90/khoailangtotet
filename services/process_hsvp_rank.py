import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)

from datamodels.crms.qlt_hsvp_xhdn import  *
from datamodels.crms.qlt_params import *
from datamodels.crms.qlt_thongtins import QLT_THONGTINVIPHAM
from typing import List
from services.crmsservices import *
from utils.constants import *

class process_rank_hsvp:
    def __init__(self, _lstHSVPs: [], _params_hsvp: {}):
        self._hsvp_params = _params_hsvp
        self._HSVPs: List[QLT_THONGTINVIPHAM] = _lstHSVPs

    def process_qlt_hsvp_xhdn(self):
        _qlt_hsvp_xhdns: List[qlt_hsvp_xhdn] = []

        logger.info("========Bắt đầu group tiêu chí HSVP========")
        _qlt_tieuchi_hsvps =  self.qlt_tieuchi_hsvps()
        logger.info("========Kết thúc group tiêu chí HSVP========")

        for item in _qlt_tieuchi_hsvps:
            kl = qlt_hsvp_xhdn(item.MA_DN, item, self._hsvp_params)
            _qlt_hsvp_xhdns.append(kl)

        return _qlt_hsvp_xhdns

    ## sẽ tối ưu chỗ này : dùng for hơi chậm chuyển thành groupby nhanh vãi
    #@property
    def qlt_tieuchi_hsvps(self):
        _qlt_tieuchi_hsvps: List[qlt_tieuchi_hsvp] = []
        #_lst_distinct = list(set([item.MA_DN for item in self._HSVPs]))
        _dict_sotk_tq = {item.MA_DN: item.SOTOKHAIDUOCTHONGQUAN for item in self._hsvp_params[const_hsvp_params.QLT_HSVP_SOTOKHAIDUOCTHONGQUAN] }

        ## sắp xếp lại theo giá trị _HSVPs theo MA_DN thì mới group by đc, mịa python ngu hơn C# =)):
        self._HSVPs.sort(key=lambda k: k.MA_DN, reverse=False)
        _group_datas = groupby(self._HSVPs, lambda f: f.MA_DN)
        for k, v in _group_datas:
            kl = qlt_tieuchi_hsvp()
            kl.MA_DN = k
            tmp = _dict_sotk_tq.get(k)
            if tmp:
                kl.SOTOKHAIDUOCTHONGQUAN = tmp
            kl.QLT_THONGTINVIPHAMs = list(v)

            _qlt_tieuchi_hsvps.append(kl)
        #_qlt_tieuchi_hsvps = [self.fx(ma_dn,_dict_sotk_tq) for ma_dn in _lst_distinct]
        return _qlt_tieuchi_hsvps

    def fx(self, _ma_dn: str,_dict_sotk_tq: {}):
        kl = qlt_tieuchi_hsvp()
        kl.MA_DN = _ma_dn
        kl.QLT_THONGTINVIPHAMs =[item for item in self._HSVPs if item.MA_DN == _ma_dn] # list(self.filterbyma_dn(_ma_dn)) #list(filter(lambda item : item.MA_DN == _ma_dn , self._HSVPs))
        #self._TMP_HSVPs = [item for item in self._TMP_HSVPs if item.MA_DN != _ma_dn]
        #print(len(self._TMP_HSVPs))
        tmp = _dict_sotk_tq.get(kl.MA_DN)
        if tmp:
            kl.SOTOKHAIDUOCTHONGQUAN = tmp
        return kl

    def filterbyma_dn(self, _ma_dn):
        for el in self._HSVPs:
            if el.MA_DN == _ma_dn: yield el


