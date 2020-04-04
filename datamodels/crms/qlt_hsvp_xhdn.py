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
    def __init__(self, _MA_DN: str, _qlt_tieuchi_hsvp, _params_hsvp : {}):
        self.MA_DN = _MA_DN
        self._qlt_tieuchi_hsvps: qlt_tieuchi_hsvp = _qlt_tieuchi_hsvp
        self._hsvp_params = _params_hsvp

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
        kl.SOLUONG_COTK = len([item for item in self._qlt_tieuchi_hsvps.QLT_THONGTINVIPHAMs if item.COTK == const_crms.CO_TK])
        kl.SOLUONG_KHONGTK = len([item for item in self._qlt_tieuchi_hsvps.QLT_THONGTINVIPHAMs if item.COTK != const_crms.CO_TK])

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
        ## tạm thời không dùng vì chưa hiểu sao unicode làm key bị remove ( LOAIVIPHAM có unicode : 127d15k4đ ...
        ##params_plvp = {(str(item.NK_XK), item.LOAIVIPHAM ): item for item in  self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVP]}

        params_plclt: List[QLT_PARAMS_HSVP_PLCLT] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLCLT]
        ## sắp xếp lại theo giá trị của bảng params_plclt:
        params_plclt.sort(key=lambda k: k.GIATRI, reverse=False)

        params_plhsvp: List[QLT_PARAMS_HSVP_PLHSVP] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLHSVP]
        ## sắp xếp lại theo giá trị của bảng params_plclt:
        params_plhsvp.sort(key=lambda k: k.ID_PHANLOAIVIPHAM, reverse=False)

        params_hspltn: List[QLT_PARAMS_HSVP_HSPLTN] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_HSPLTN]
        ## sắp xếp lại theo giá trị của bảng params_hspltn:
        params_hspltn.sort(key=lambda k: k.ID_TRACHNHIEM, reverse=False)

        ## lấy những vp có tờ khai, vi phạm ko có tờ khai tính ở qlt_hsvp_tokhais (NK_XK=3)
        _lst_tieuchi_hsvps_coTK: List[QLT_THONGTINVIPHAM] = [item for item in self._qlt_tieuchi_hsvps.QLT_THONGTINVIPHAMs if item.COTK == const_crms.CO_TK]

        _tmp_qlt_hsvp_nhoms: List[qlt_hsvp_nhom] = []
        for item in _lst_tieuchi_hsvps_coTK:
            for NK_XK in [1,2] : ## đoạn này code cũ đang fix NK_XK , phải hỏi thêm xem , phải lấy XK_NK từ item.XK_NK mới đúng(bảng QLT_THONGTINVIPHAM)

                kl = qlt_hsvp_nhom()
                kl.NK_XK = NK_XK #item.NK_XK
                #print("NK_XK:{} LOAIVIPHAM: {}".format(item.NK_XK, item.LOAIVIPHAM))
                tmp = None
                #_lst_tmp = [i for i in self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVP] if i.NK_XK == item.NK_XK and  i.LOAIVIPHAM == item.LOAIVIPHAM ]
                _lst_tmp = [i for i in self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLVP] if
                            i.NK_XK == NK_XK and i.LOAIVIPHAM == item.LOAIVIPHAM]
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


    #@property
    def qlt_hsvp_phanloai_nhoms(self):
        _qlt_hsvp_phanloai_nhoms: List[qlt_hsvp_phanloai_nhom] = []
        params_plslvp: List[QLT_PARAMS_HSVP_PLSLVP] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLSLVP]

        for dpln in self.qlt_hsvp_nhoms():
            kl = qlt_hsvp_phanloai_nhom()
            kl.ID_NHOM = dpln.ID_NHOM
            kl.NK_XK = dpln.NK_XK
            _params_plslvp: List[QLT_PARAMS_HSVP_PLSLVP] = [p for p in params_plslvp
                                                            if p.NK_XK == dpln.NK_XK and p.ID_NHOM == dpln.ID_NHOM
                                                            ]
            ## sắp xếp lại theo giá trị của bảng PLCC:
            _params_plslvp.sort(key=lambda k: k.GIATRI, reverse=False)
            for item in _params_plslvp:
                if dpln.SOLUONG_NHOM <= item.GIATRI:
                    kl.DIEMNHOM = item.DIEM
                    break
            _qlt_hsvp_phanloai_nhoms.append(kl)

        return _qlt_hsvp_phanloai_nhoms

    #@property
    def qlt_hsvp_tytrong_nhoms(self):
        _qlt_hsvp_tytrong_nhoms: List[qlt_hsvp_tytrong_nhom] = []
        _soluong_tktq = self.qlt_hsvp_tokhais.SOLUONG_COTK + self.qlt_hsvp_tokhais.SOLUONG_KHONGTK
        if self._qlt_tieuchi_hsvps.SOTOKHAIDUOCTHONGQUAN > _soluong_tktq:
            _soluong_tktq = self._qlt_tieuchi_hsvps.SOTOKHAIDUOCTHONGQUAN


        for item in self.qlt_hsvp_nhoms():
            kl = qlt_hsvp_tytrong_nhom()
            kl.ID_NHOM = item.ID_NHOM
            kl.NK_XK = item.NK_XK
            kl.TYTRONG =min((item.SOLUONG_NHOM/_soluong_tktq)*100, 100 )
            _qlt_hsvp_tytrong_nhoms.append(kl)

        return _qlt_hsvp_tytrong_nhoms


    #@property
    def qlt_hsvp_tyle_nhoms(self):
        _qlt_hsvp_tyle_nhoms: List[qlt_hsvp_tyle_nhom] = []
        params_pltlvp = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_PLTLVP]
        for ttpl in self.qlt_hsvp_tytrong_nhoms():
            kl = qlt_hsvp_tyle_nhom()
            kl.NK_XK = ttpl.NK_XK
            kl.ID_NHOM = ttpl.ID_NHOM
            _params_pltlvp: List[QLT_PARAMS_HSVP_PLTLVP] = [p for p in params_pltlvp
                                                           if p.NK_XK == ttpl.NK_XK and p.ID_NHOM == ttpl.ID_NHOM
                                                            ]
            ## sắp xếp lại theo giá trị của bảng PLCC:
            _params_pltlvp.sort(key=lambda k: k.GIATRI, reverse=False)
            for item in _params_pltlvp:
                if ttpl.TYTRONG <= item.GIATRI:
                    kl.TYLE = item.TYLEPHANLOAI
                    break

            _qlt_hsvp_tyle_nhoms.append(kl)

        return _qlt_hsvp_tyle_nhoms

    #// Step 6: Nhan diem phan loai nhom * ty le phan loai nhom (vi pham co to khai) ( trước khi cộng vp không tờ khai)
    #@property
    def DIEM_PLVP_TRUOCCONG(self):
        _DIEM_PLVP_TRUOCCONG = {}
        _dplnhoms = self.qlt_hsvp_phanloai_nhoms()
        _tlplnhoms = self.qlt_hsvp_tyle_nhoms()
        _dict_dplnhoms = {(item.NK_XK, item.ID_NHOM): item.DIEMNHOM for item in _dplnhoms}
        _dict_tlplnhoms = {(item.NK_XK, item.ID_NHOM): item.TYLE for item in _tlplnhoms}
        _DIEM_PLVP_TRUOCCONG_NK = 0.0
        _DIEM_PLVP_TRUOCCONG_XK = 0.0
        for key, value in _dict_dplnhoms.items():
            if key[0] == const_crms.LOAI_HINH_NK:
                _DIEM_PLVP_TRUOCCONG_NK += (value * _dict_tlplnhoms[key])/100
            else:
                _DIEM_PLVP_TRUOCCONG_XK += (value * _dict_tlplnhoms[key])/100

        _DIEM_PLVP_TRUOCCONG[const_crms.LOAI_HINH_NK] = _DIEM_PLVP_TRUOCCONG_NK
        _DIEM_PLVP_TRUOCCONG[const_crms.LOAI_HINH_XK] = _DIEM_PLVP_TRUOCCONG_XK

        return _DIEM_PLVP_TRUOCCONG


    #// Step 7: Diem phan loai vi pham + Diem phan loai vi pham khong co to khai
    #@property
    def DIEM_PLVP(self):
        _DIEM_PLVP_TRUOCCONG = self.DIEM_PLVP_TRUOCCONG()
        _DIEM_PLVP = {}
        diem_ktokhai = self.qlt_hsvp_tokhais
        _DIEM_PLVP[const_crms.LOAI_HINH_NK] = _DIEM_PLVP_TRUOCCONG[const_crms.LOAI_HINH_NK] + diem_ktokhai.DIEM_KHONGTK
        _DIEM_PLVP[const_crms.LOAI_HINH_XK] = _DIEM_PLVP_TRUOCCONG[const_crms.LOAI_HINH_XK] + diem_ktokhai.DIEM_KHONGTK

        return _DIEM_PLVP

    #// Step 8: Diem phan loai vi pham * he so phan loai XK, NK
    #@property
    def DIEM_PLVP_NHANHESO(self):
        _DIEM_PLVP_NHANHESO = {}
        _DIEM_PLVP = self.DIEM_PLVP()
        _params_hsplxnk: List[QLT_PARAMS_HSVP_HSPLXNK] = self._hsvp_params[const_hsvp_params.QLT_PARAMS_HSVP_HSPLXNK]
        _hs_NK = [item.HESO for item in _params_hsplxnk if item.NK_XK == const_crms.LOAI_HINH_NK][0]
        _hs_XK = [item.HESO for item in _params_hsplxnk if item.NK_XK == const_crms.LOAI_HINH_XK][0]

        _DIEM_PLVP_NHANHESO[const_crms.LOAI_HINH_NK] = _DIEM_PLVP[const_crms.LOAI_HINH_NK] * _hs_NK
        _DIEM_PLVP_NHANHESO[const_crms.LOAI_HINH_XK] = _DIEM_PLVP[const_crms.LOAI_HINH_XK] * _hs_XK

        return _DIEM_PLVP_NHANHESO

    #// Step 9: Diem phan loai vi pham NK trc khi cong + Diem phan loai vi pham XK da nhan he so
    @property
    def DIEM_PLCC(self):
        _DIEM_PLVP = self.DIEM_PLVP()
        _DIEM_PLVP_NHANHESO = self.DIEM_PLVP_NHANHESO()
        _kl = qlt_hsvp_diemplcc()
        _kl.DIEM_PLCC_NK = _DIEM_PLVP[const_crms.LOAI_HINH_NK] + _DIEM_PLVP_NHANHESO[const_crms.LOAI_HINH_NK]
        _kl.DIEM_PLCC_XK = _DIEM_PLVP[const_crms.LOAI_HINH_XK] + _DIEM_PLVP_NHANHESO[const_crms.LOAI_HINH_XK]

        return _kl


class qlt_tieuchi_hsvp:
    def __init__(self):
        self.MA_DN=""
        self.QLT_THONGTINVIPHAMs: List[QLT_THONGTINVIPHAM] = []
        self.SOTOKHAIDUOCTHONGQUAN = 0

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

class qlt_hsvp_diemplcc:
    def __init__(self):
        self.DIEM_PLCC_NK = 0.0
        self.DIEM_PLCC_XK = 0.0

