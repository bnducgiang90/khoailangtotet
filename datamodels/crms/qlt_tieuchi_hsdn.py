import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)
from typing import List, Dict
from itertools import groupby
from collections import Counter
from utils.constants import *
from datamodels.crms.qlt_tieuchi_hsdn import  *
from datamodels.crms.qlt_params import *

class qlt_hsdn_xhdn:
    def __init__(self, _MA_DN: str, _qlt_tieuchi_hsdns: []):
        self.MA_DN = _MA_DN
        self.qlt_tieuchi_hsdns: List[qlt_tieuchi_hsdn] = _qlt_tieuchi_hsdns
        self.qlt_tieuchi_nhoms: List[qlt_tieuchi_nhom] = []
        self.qlt_tieuchi_max_nhoms: List[qlt_tieuchi_nhom] = []
        self.qlt_tytrong_phanloai_nhoms: List[qlt_tytrong_phanloai_nhom] = []
        self.qlt_diem_phanloaicuoicung_nhoms: List[qlt_diem_phanloaicuoicung_nhom] = []


    def get_qlt_tieuchi_nhoms(self):
        list_tmp = []

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM)]]
        for i, g in groupby(self.qlt_tieuchi_hsdns, key=lambda x: (x.ID_NHOM, x.NK_XK)):
            list_tmp.append([i, sum(v.DIEM for v in g)])

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEMNHOM - đã group]]
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

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEM)]]
        for i, g in groupby(self.qlt_tieuchi_hsdns, key=lambda x: (x.ID_NHOM, x.NK_XK)):
            list_tmp.append([i, sum(v.DIEM_MAX for v in g)])

        ## OUTPUT : [ [(ID_NHOM,NK_XK),DIEMNHOM - đã group]]
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

        # {key=(NK_XK,ID_NHOM), value= DIEMNHOM)}
        dict_nhoms = {(item.NK_XK,item.ID_NHOM): item.DIEMNHOM for item in lst_nhoms}

        # {key=(NK_XK,ID_NHOM), value= DIEMNHOM)}
        dict_max_nhoms = {(item.NK_XK,item.ID_NHOM): item.DIEMNHOM for item in lst_max_nhoms}

        for key, value in dict_nhoms.items():
            objqlt_tytrong_phanloai_nhom = qlt_tytrong_phanloai_nhom()
            objqlt_tytrong_phanloai_nhom.ID_NHOM = key[1]
            objqlt_tytrong_phanloai_nhom.NK_XK = key[0]
            objqlt_tytrong_phanloai_nhom.TYTRONG = (value/dict_max_nhoms[key])* 100

            self.qlt_tytrong_phanloai_nhoms.append(objqlt_tytrong_phanloai_nhom)
        return self.qlt_tytrong_phanloai_nhoms

    def get_qlt_diem_phanloaicuoicung_nhoms(self, params_hsdn : {}):
        lst_tytrong_phanloais: List[qlt_tytrong_phanloai_nhom] = self.get_qlt_tytrong_phanloai_nhoms()
        params_hsdn_dplcc: List[QLT_PARAMS_HSDN_PLDCC] = [] #params_hsdn[const_hsdn_params.QLT_PARAMS_HSDN_PLDCC]

        ##tính toán điểm PLCC:
        for ttpl in lst_tytrong_phanloais:
            obj_qlt_diem_phanloaicuoicung_nhom = qlt_diem_phanloaicuoicung_nhom()
            obj_qlt_diem_phanloaicuoicung_nhom.NK_XK = ttpl.NK_XK
            obj_qlt_diem_phanloaicuoicung_nhom.ID_NHOM = ttpl.ID_NHOM
            obj_qlt_diem_phanloaicuoicung_nhom.DIEM_PLCC = None

            params_hsdn_dplcc = [item for item in params_hsdn[const_hsdn_params.QLT_PARAMS_HSDN_PLDCC] if item.NK_XK == ttpl.NK_XK and item.ID_NHOM == ttpl.ID_NHOM]

            ## sắp xếp lại theo giá trị của bảng PLCC:
            params_hsdn_dplcc.sort(key=lambda item: item.GIATRI, reverse=False)

            for item in params_hsdn_dplcc:
                if ttpl.TYTRONG <= item.GIATRI:
                    obj_qlt_diem_phanloaicuoicung_nhom.DIEM_PLCC = item.DIEM
                    break;
            if obj_qlt_diem_phanloaicuoicung_nhom.DIEM_PLCC is None :
                logger.warning("NK_XK : {} ; ID_NHOM :{} có giá trị {} không phù hợp với bảng tham số QLT_PARAMS_HSDN_PLDCC có giá trị MAX là {} "
                               .format(ttpl.NK_XK, ttpl.ID_NHOM,
                                       ttpl.TYTRONG, params_hsdn_dplcc[-1].GIATRI)
                               )
            self.qlt_diem_phanloaicuoicung_nhoms.append(obj_qlt_diem_phanloaicuoicung_nhom)

        return self.qlt_diem_phanloaicuoicung_nhoms

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