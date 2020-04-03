import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)
from typing import List, Dict
#from itertools import groupby
from collections import Counter
from utils.constants import *
from datamodels.crms.qlt_params import *

class qlt_hsdn_xhdn:
    def __init__(self, _MA_DN: str, _qlt_tieuchi_hsdns: [], _lst_params_pldcc:[]):
        self.MA_DN = _MA_DN
        self.qlt_tieuchi_hsdns: List[qlt_tieuchi_hsdn] = _qlt_tieuchi_hsdns
        self.lst_params_pldcc: List[QLT_PARAMS_HSDN_PLDCC] = _lst_params_pldcc
        # self.qlt_tieuchi_nhoms: List[qlt_tieuchi_nhom] = []
        # self.qlt_tieuchi_max_nhoms: List[qlt_tieuchi_nhom] = []
        # self.qlt_tytrong_phanloai_nhoms: List[qlt_tytrong_phanloai_nhom] = []
        # self.qlt_diem_phanloaicuoicung_nhoms: List[qlt_diem_phanloaicuoicung_nhom] = []

    @property
    def DIEM_PLCC(self):
        _kl = qlt_hsdn_diemplcc()
        _dlpcc_nhoms = self.qlt_diem_phanloaicuoicung_nhoms
        _kl.DIEM_PLCC_NK = sum([item.DIEM_PLCC for item in _dlpcc_nhoms if item.NK_XK == const_crms.LOAI_HINH_NK])
        _kl.DIEM_PLCC_XK = sum([item.DIEM_PLCC for item in _dlpcc_nhoms if item.NK_XK == const_crms.LOAI_HINH_XK])
        _kl.DIEM_PHAT_NK = sum([item.DIEMPHAT for item in self.qlt_tieuchi_hsdns  if item.NK_XK == const_crms.LOAI_HINH_NK and item.DIEMPHAT is not None ])
        _kl.DIEM_PHAT_XK = sum([item.DIEMPHAT for item in self.qlt_tieuchi_hsdns if item.NK_XK == const_crms.LOAI_HINH_XK and item.DIEMPHAT is not None])

        return _kl


    @property
    def qlt_tieuchi_nhoms(self):
        # list_tmp = []
        _qlt_tieuchi_nhoms: List[qlt_tieuchi_nhom] = []

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM)]]
        list_tmp = [[(x.ID_NHOM, x.NK_XK), x.DIEM] for x in self.qlt_tieuchi_hsdns]

        ''' dùng group by
        print("list_tmp:")
        print(list_tmp)
        list_tmp2 =[]
        for i, g in groupby(sorted(list_tmp), key=lambda x : x[0]):
            list_tmp2.append([i, sum(v[1] for v in g)])
        print("list_tmp2:")
        print(list_tmp2)

        '''
        ## dùng Counter
        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEMNHOM - đã group]]
        list_tmp = list(Counter(key for key, DIEM in list_tmp for idx in range(DIEM)).items())


        for item in list_tmp:
            kl = qlt_tieuchi_nhom()
            kl.ID_NHOM = item[0][0]
            kl.NK_XK = item[0][1]
            kl.DIEMNHOM = item[1]
            _qlt_tieuchi_nhoms.append(kl)

        return _qlt_tieuchi_nhoms

    @property
    def qlt_tieuchi_max_nhoms(self):
        list_tmp = []
        _qlt_tieuchi_max_nhoms: List[qlt_tieuchi_nhom] = []

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM)]]
        list_tmp = [[(x.ID_NHOM, x.NK_XK), x.DIEM_MAX] for x in self.qlt_tieuchi_hsdns]

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM_MAX - đã group]]
        list_tmp = list(Counter(key for key, DIEM_MAX in list_tmp for idx in range(DIEM_MAX)).items())

        for item in list_tmp:
            kl = qlt_tieuchi_nhom()
            kl.ID_NHOM = item[0][0]
            kl.NK_XK = item[0][1]
            kl.DIEMNHOM = item[1]
            _qlt_tieuchi_max_nhoms.append(kl)

        return _qlt_tieuchi_max_nhoms

    @property
    def qlt_tytrong_phanloai_nhoms(self):
        _lst_nhoms = self.qlt_tieuchi_nhoms
        _lst_max_nhoms = self.qlt_tieuchi_max_nhoms
        _qlt_tytrong_phanloai_nhoms: List[qlt_tytrong_phanloai_nhom] = []

        # {key=(NK_XK,ID_NHOM), value= DIEMNHOM)}
        dict_nhoms = {(item.NK_XK,item.ID_NHOM): item.DIEMNHOM for item in _lst_nhoms}

        # {key=(NK_XK,ID_NHOM), value= DIEMNHOM)}
        dict_max_nhoms = {(item.NK_XK,item.ID_NHOM): item.DIEMNHOM for item in _lst_max_nhoms}

        for key, value in dict_nhoms.items():
            kl = qlt_tytrong_phanloai_nhom()
            kl.ID_NHOM = key[1]
            kl.NK_XK = key[0]
            kl.TYTRONG = (value/dict_max_nhoms[key])* 100

            _qlt_tytrong_phanloai_nhoms.append(kl)
        return _qlt_tytrong_phanloai_nhoms

    @property
    def qlt_diem_phanloaicuoicung_nhoms(self):
        _lst_tytrong_phanloais: List[qlt_tytrong_phanloai_nhom] = self.qlt_tytrong_phanloai_nhoms
        _qlt_diem_phanloaicuoicung_nhoms: List[qlt_diem_phanloaicuoicung_nhom] = []

        ##tính toán điểm PLCC:
        for ttpl in _lst_tytrong_phanloais:
            kl = qlt_diem_phanloaicuoicung_nhom()
            kl.NK_XK = ttpl.NK_XK
            kl.ID_NHOM = ttpl.ID_NHOM
            kl.DIEM_PLCC = None
            params_hsdn_dplcc: List[QLT_PARAMS_HSDN_PLDCC]  = [item for item in self.lst_params_pldcc
                                                                if item.NK_XK == ttpl.NK_XK and item.ID_NHOM == ttpl.ID_NHOM
                                                               ]
            ## sắp xếp lại theo giá trị của bảng PLCC:
            params_hsdn_dplcc.sort(key=lambda item: item.GIATRI, reverse=False)

            for item in params_hsdn_dplcc:
                if ttpl.TYTRONG <= item.GIATRI:
                    kl.DIEM_PLCC = item.DIEM
                    # if kl.NK_XK == const_crms.LOAI_HINH_NK: self._DIEM_PLCC_NK += item.DIEM
                    # else : self._DIEM_PLCC_XK += item.DIEM
                    break

            if kl.DIEM_PLCC is None :
                logger.warning("NK_XK : {} ; ID_NHOM :{} có giá trị {} không phù hợp với bảng tham số QLT_PARAMS_HSDN_PLDCC có giá trị MAX là {} "
                               .format(ttpl.NK_XK, ttpl.ID_NHOM,
                                       ttpl.TYTRONG, params_hsdn_dplcc[-1].GIATRI)
                               )

            _qlt_diem_phanloaicuoicung_nhoms.append(kl)

        return _qlt_diem_phanloaicuoicung_nhoms

class qlt_tieuchi_hsdn:
    def __init__(self):
        self.MA_DN=""
        self.ID_TIEUCHI = None
        self.GIA_TRI = None
        self.ID_NHOM = None
        self.NK_XK = None
        self.PHUONGTHUCAPDUNG = None
        self.DIEM = None
        self.DIEMPHAT = None

        ## điểm phân loại lớn nhất của tiêu chí
        self.DIEM_MAX = None

class qlt_tieuchi_nhom:
    def __init__(self):
        self.ID_NHOM = None
        self.NK_XK = None
        self.DIEMNHOM = None

class qlt_tytrong_phanloai_nhom:
    def __init__(self):
        self.ID_NHOM = None
        self.NK_XK = None
        self.TYTRONG = 0.0

class qlt_diem_phanloaicuoicung_nhom:
    def __init__(self):
        self.ID_NHOM = None
        self.NK_XK = None
        self.DIEM_PLCC = 0.0

class qlt_hsdn_diemplcc:
    def __init__(self):
        self.DIEM_PLCC_NK = 0.0
        self.DIEM_PLCC_XK = 0.0
        self.DIEM_PHAT_NK = 0.0
        self.DIEM_PHAT_XK = 0.0