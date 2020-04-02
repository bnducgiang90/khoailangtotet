import sys

from pyparsing import unicode

sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)
from typing import List, Dict
from itertools import groupby
from collections import Counter
from utils.constants import *
from datamodels.crms.qlt_params import *
from datamodels.crms.qlt_thongtins import  QLT_THONGTINVIPHAM

class qlt_hsvp_xhdn:
    def __init__(self, _MA_DN: str, _qlt_tieuchi_hsvps: [], _params_hsvp : {}):
        self.MA_DN = _MA_DN
        self._qlt_tieuchi_hsvps: List[QLT_THONGTINVIPHAM] = _qlt_tieuchi_hsvps
        self._hsvp_params = _params_hsvp
        self._DIEM_PLCC_NK = 0
        self._DIEM_PLCC_XK = 0
        self._DIEM_PLVP_NK = 0.0
        self._DIEM_PLVP_XK = 0.0
        self._DIEM_PLVP_TRUOCCONG_NK = 0.0
        self._DIEM_PLVP_TRUOCCONG_XK = 0.0
        self._DIEM_PLVP_NHANHESO_NK = 0.0
        self._DIEM_PLVP_NHANHESO_XK = 0.0

    def get_giatri_thoaman(self, giatri, lst:[]):
        kl = None
        for i in lst:
            if giatri <= i:
                kl = i
                break
        if kl is None:
            logger.warning("qlt_hsvp_xhdn:get_giatri_thoaman giá trị {} không thỏa mãn danh sách có giá trị max {}".format(i, lst[-1]))

        return kl

    @property
    def qlt_hsvp_tokhais(self):
        kl = qlt_hsvp_tokhai()
        kl.SOLUONG_COTK = len([item for item in self._qlt_tieuchi_hsvps if item.COTK == const_crms.CO_TK])
        kl.SOLUONG_KHONGTK = len([item for item in self._qlt_tieuchi_hsvps if item.COTK != const_crms.CO_TK])

        for p in self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVPKTK]:
            if kl.SOLUONG_KHONGTK <= p.GIATRI:
                kl.DIEM_KHONGTK = p.DIEM
                break;

        return kl

    ## Hàm này hiện đang dài quá, sẽ viết ngắn gọn lại sau:
    #@property
    def qlt_hsvp_nhoms(self):
        _qlt_hsvp_nhoms: List[qlt_hsvp_nhom] = []

        ## (str(item.NK_XK), item.LOAIVIPHAM) : phải convert sang string thì dictionary mới sử dụng tuple là key đc:
        ## tuple là key của dict thì các item của tuple phải cùng kiểu
        ## tạm thời không dùng vì python không cho phép unicode làm key ( LOAIVIPHAM có unicode : 127d15k4đ ...
        #params_plvp = {(str(item.NK_XK), item.LOAIVIPHAM ): item for item in  self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVP]}

        params_plclt: List[QLT_PARAMS_HSVP_PLCLT] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLCLT]
        params_plhsvp: List[QLT_PARAMS_HSVP_PLHSVP] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLHSVP]
        params_hspltn: List[QLT_PARAMS_HSVP_HSPLTN] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_HSPLTN]

        ## lấy những vp có tờ khai, vi phạm ko có tờ khai tính ở qlt_hsvp_tokhais (NK_XK=3)
        _lst_tieuchi_hsvps_coTK: List[QLT_THONGTINVIPHAM] = [item for item in self._qlt_tieuchi_hsvps if item.COTK == const_crms.CO_TK]

        _tmp_qlt_hsvp_nhoms: List[qlt_hsvp_nhom] = []
        for item in _lst_tieuchi_hsvps_coTK:
            kl = qlt_hsvp_nhom()
            kl.NK_XK = item.NK_XK
            print("NK_XK:{} LOAIVIPHAM: {}".format(item.NK_XK, item.LOAIVIPHAM))
            tmp = None
            _lst_tmp = [i for i in self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVP] if i.NK_XK == item.NK_XK and  i.LOAIVIPHAM == item.LOAIVIPHAM ]
            if len(_lst_tmp) >0:
                tmp = _lst_tmp[0]

            if tmp:
                if tmp.ISAPDUNGCHENHLECHTHUE == const_crms.ISAPDUNGCHENHLECHTHUE:
                    # tính ID_NHOM: theo bảng QLT_PARAMS_HSVP_PLCLT
                    for p in params_plclt:
                        if item.TONG_CHENHLECHTHUE <= p.GIATRI:
                            kl.ID_NHOM = p.ID_NHOM
                            break;
                else:
                    # tính ID_NHOM: theo bảng QLT_PARAMS_HSVP_PLVP
                    kl.ID_NHOM = tmp.ID_NHOM
            else:
                kl.ID_NHOM = const_crms.ID_NHOM_DEFAULT

            # tính HSPLVP:
            for p in params_plhsvp:
                if item.NGHIEMTRONG <= p.ID_PHANLOAIVIPHAM:
                    kl.HSPLVP = p.HESO
                    break;
            # tính HSPLTN:
            for p in params_hspltn:
                if item.TRACHNHIEM <= p.ID_TRACHNHIEM:
                    kl.HSPLTN = p.HESO
                    break

            kl.SOLUONG_NHOM = kl.HSPLTN * kl.HSPLVP
            _tmp_qlt_hsvp_nhoms.append(kl)

        ##group nhóm:
        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM)]]
        list_tmp = [[(x.ID_NHOM, x.NK_XK), x.SOLUONG_NHOM] for x in _tmp_qlt_hsvp_nhoms]

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM_MAX - đã group]]
        list_tmp2 = []
        for i, g in groupby(sorted(list_tmp), key=lambda x: x[0]):
            list_tmp2.append([i, sum(v[1] for v in g)])


        for item in list_tmp2:
            kl = qlt_hsvp_nhom()
            kl.ID_NHOM = item[0][0]
            kl.NK_XK = item[0][1]
            kl.SOLUONG_NHOM = item[1]
            _qlt_hsvp_nhoms.append(kl)

        #_qlt_hsvp_nhoms = _tmp_qlt_hsvp_nhoms

        return _qlt_hsvp_nhoms;


    @property
    def qlt_hsvp_phanloai_nhoms(self):
        pass

    @property
    def qlt_hsvp_tytrong_nhoms(self):
        pass

    @property
    def qlt_hsvp_tyle_nhoms(self):
        pass

    @property
    def qlt_hsvp_tyle_nhoms(self):
        pass

    #// Step 6: Nhan diem phan loai nhom * ty le phan loai nhom (vi pham co to khai)
    @property
    def DIEM_PLVP_NK(self):
        pass

    @property
    def DIEM_PLVP_XK(self):
        pass

    #// Step 7: Diem phan loai vi pham + Diem phan loai vi pham khong co to khai
    @property
    def DIEM_PLVP_TRUOCCONG_NK(self):
        pass

    @property
    def DIEM_PLVP_TRUOCCONG_XK(self):
        pass

    #// Step 8: Diem phan loai vi pham * he so phan loai XK, NK
    @property
    def DIEM_PLVP_NHANHESO_NK(self):
        pass

    @property
    def DIEM_PLVP_NHANHESO_XK(self):
        pass

    #// Step 9: Diem phan loai vi pham NK trc khi cong + Diem phan loai vi pham XK da nhan he so
    @property
    def DIEM_PLCC_NK(self):
        pass

    @property
    def DIEM_PLCC_XK(self):
        pass


class qlt_tieuchi_hsvp:
    def __init__(self):
        self.MA_DN=""
        self.QLT_THONGTINVIPHAMs: List[QLT_THONGTINVIPHAM] = []

class qlt_hsvp_tokhai:
    def __init__(self):
        self.SOLUONG_COTK = 0
        self.SOLUONG_KHONGTK = 0
        self.DIEM_COTK = 0.0
        self.DIEM_KHONGTK = 0.0

class qlt_hsvp_nhom:
    def __init__(self):
        self.ID_NHOM = ""
        self.NK_XK = None
        self.HSPLVP = 0.0
        self.HSPLTN = 0.0
        self.SOLUONG_NHOM = 0.0


    #
    # @property
    # def SOLUONG_NHOM(self):
    #     if self.HSPLVP == 0 : self.HSPLVP = 1
    #     if self.HSPLTN == 0 : self.HSPLTN = 1
    #     return self.HSPLVP * self.HSPLVP

class qlt_hsvp_phanloai_nhom:
    def __init__(self):
        self.ID_NHOM = ""
        self.NK_XK = None
        self.DIEMNHOM = None

class qlt_hsvp_tytrong_nhom:
    def __init__(self):
        self.ID_NHOM = ""
        self.NK_XK = None
        self.TYTRONG = 0.0

class qlt_hsvp_tyle_nhom:
    def __init__(self):
        self.ID_NHOM = ""
        self.NK_XK = None
        self.TYLE = 0.0

