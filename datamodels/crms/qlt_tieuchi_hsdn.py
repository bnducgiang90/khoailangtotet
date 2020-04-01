import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)
from typing import List, Dict
from itertools import groupby
from collections import Counter

class qlt_hsdn_xhdn:
    def __init__(self, _MA_DN: str, _qlt_tieuchi_hsdns: []):
        self.MA_DN = _MA_DN
        self.qlt_tieuchi_hsdns: List[qlt_tieuchi_hsdn] = _qlt_tieuchi_hsdns
        self.qlt_tieuchi_nhoms: List[qlt_tieuchi_nhom] = []
        self.qlt_tieuchi_max_nhoms: List[qlt_tieuchi_nhom] = []
        self.qlt_tytrong_phanloai_nhoms: List[qlt_tytrong_phanloai_nhom] = []

    def get_qlt_tieuchi_nhoms(self):
        list_tmp = []
        for i, g in groupby(self.qlt_tieuchi_hsdns, key=lambda x: (x.ID_NHOM, x.NK_XK)):
            list_tmp.append([i, sum(v.DIEM for v in g)])

        list_tmp = list(Counter(key for key, num in list_tmp
                      for idx in range(num)).items())

        for item in list_tmp:
            objqlt_tieuchi_nhom = qlt_tieuchi_nhom()
            objqlt_tieuchi_nhom.ID_NHOM = item[0][0]
            objqlt_tieuchi_nhom.NK_XK = item[0][1]
            objqlt_tieuchi_nhom.DIEMNHOM = item[1]
            self.qlt_tieuchi_nhoms.append(objqlt_tieuchi_nhom)

        return self.qlt_tieuchi_nhoms

    def get_qlt_tieuchi_max_nhoms(self):
        list_tmp = []
        for i, g in groupby(self.qlt_tieuchi_hsdns, key=lambda x: (x.ID_NHOM, x.NK_XK)):
            list_tmp.append([i, sum(v.DIEM_MAX for v in g)])

        list_tmp = list(Counter(key for key, num in list_tmp
                      for idx in range(num)).items())

        for item in list_tmp:
            objqlt_tieuchi_max_nhom = qlt_tieuchi_nhom()
            objqlt_tieuchi_max_nhom.ID_NHOM = item[0][0]
            objqlt_tieuchi_max_nhom.NK_XK = item[0][1]
            objqlt_tieuchi_max_nhom.DIEMNHOM = item[1]
            self.qlt_tieuchi_max_nhoms.append(objqlt_tieuchi_max_nhom)

        return self.qlt_tieuchi_max_nhoms

    def get_qlt_tytrong_phanloai_nhoms(self):
        lst_nhoms = self.get_qlt_tieuchi_nhoms()
        lst_max_nhoms = self.get_qlt_tieuchi_max_nhoms()
        dict_nhoms = {(item.NK_XK,item.ID_NHOM): item.DIEMNHOM for item in lst_nhoms}
        dict_max_nhoms = {(item.NK_XK,item.ID_NHOM): item.DIEMNHOM for item in lst_max_nhoms}

        for key, value in dict_nhoms.items():
            objqlt_tytrong_phanloai_nhom = qlt_tytrong_phanloai_nhom()
            objqlt_tytrong_phanloai_nhom.ID_NHOM = key[1]
            objqlt_tytrong_phanloai_nhom.NK_XK = key[0]
            objqlt_tytrong_phanloai_nhom.TYTRONG = (value/dict_max_nhoms[key])* 100

            self.qlt_tytrong_phanloai_nhoms.append(objqlt_tytrong_phanloai_nhom)
        return self.qlt_tytrong_phanloai_nhoms

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