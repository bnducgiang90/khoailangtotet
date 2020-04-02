from decimal import *

##class crms_tokhai_nothue - mapping với bảng CRMS_TOKHAI_NOTHUE
class crms_tokhai_nothue:
    def __init__(self):
        ## private varibale or property in Python
        self.ID: decimal = 0.0
        self.MA_HQXL: str = ""
        self.MA_DV: str = ""

    ## getter method to get the properties using an object
    def get_ID(self):
        return Decimal(self.ID)

    ## setter method to change the value 'a' using an object
    def set_ID(self, ID):
        self.ID = Decimal(ID)

    ## getter method to get the properties using an object
    def get_MA_HQXL(self):
        return self.MA_HQXL

    ## setter method to change the value 'a' using an object
    def set_MA_HQXL(self, MA_HQXL):
        self.MA_HQXL = MA_HQXL

    ## getter method to get the properties using an object
    def get_MA_DV(self):
        return self.MA_DV

    ## setter method to change the value 'a' using an object
    def set_MA_DV(self, MA_DV):
        self.MA_DV = MA_DV

##Thong tin các bảng params HSDN:
class QLT_PARAMS_HSDN_TC_MOTA:
    def __init__(self):
        self.ID = 0
        self.ID_TIEUCHI = 0
        self.ID_NHOM = 0
        self.MOTATIEUCHI = ""
        self.COLUMNNAME = ""
        self.ISSUDUNG = 0
        self.ISORDER = 0
        self.NK_XK = 0
        self.PHUONGTHUCAPDUNG = 0


class QLT_PARAMS_HSDN_DGTC:
    def __init__(self):
        self.ID = 0
        self.ID_TIEUCHI = 0
        self.GIATRI = 0
        self.DIEMSO = 0
        self.DIEMPHAT = 0
        self.MOTA = ""


class QLT_PARAMS_HSDN_PLDCC:
    def __init__(self):
        self.ID = 0
        self.NK_XK = 0
        self.ID_NHOM = 0
        self.GIATRI = 0.0
        self.DIEM = 0

class QLT_PARAMS_HSDN_PTAD:
    def __init__(self):
        self.ID = 0
        self.ID_TIEUCHI = 0
        self.NK_XK = 0
        self.PHUONGTHUCAPDUNG = 0

####Thong tin các bảng params HSVP:
class QLT_PARAMS_HSVP_HSPLTN:
    def __init__(self):
        self.ID = 0
        self.ID_TRACHNHIEM = 0
        self.HESO = 0.0
        self.TEN = ""

class QLT_PARAMS_HSVP_HSPLXNK:
    def __init__(self):
        self.ID = 0
        self.NK_XK = 0
        self.HESO = 0.0

class QLT_PARAMS_HSVP_PLCLT:
    def __init__(self):
        self.ID = 0
        self.GIATRI = 0
        self.ID_NHOM = ""

class QLT_PARAMS_HSVP_PLHSVP:
    def __init__(self):
        self.ID = 0
        self.ID_PHANLOAIVIPHAM = 0
        self.HESO = 0.0

class QLT_PARAMS_HSVP_PLSLVP:
    def __init__(self):
        self.ID = 0
        self.NK_XK = 0
        self.ID_NHOM = ""
        self.GIATRI = 0
        self.DIEM = 0

class QLT_PARAMS_HSVP_PLTLVP:
    def __init__(self):
        self.ID = 0
        self.NK_XK = 0
        self.ID_NHOM = ""
        self.GIATRI = 0.0
        self.TYLEPHANLOAI = 0.0

class QLT_PARAMS_HSVP_PLVP:
    def __init__(self):
        self.ID = 0
        self.NK_XK = 0
        self.LOAIVIPHAM = ""
        self.ID_NHOM = ""
        self.ISAPDUNGCHENHLECHTHUE = 0

class QLT_PARAMS_HSVP_PLVPKTK:
    def __init__(self):
        self.ID = 0
        self.GIATRI = 0.0
        self.DIEM = 0.0

class QLT_HSVP_SOTOKHAIDUOCTHONGQUAN:
    def __init__(self):
        self.MA_DN = ""
        self.SOTOKHAIDUOCTHONGQUAN = 0

class QLT_HSVP_VIPHAMTOKHAI:
    def __init__(self):
        self.MA_DN = ""
        self.SO_VP_COTK = 0
        self.SO_VP_KHONGTK = 0

## thông tin bảng params QLT_PARAMS_PLXEPHANG
class QLT_PARAMS_PLXEPHANG:
    def __init__(self):
        self.ID = 0
        self.NK_XK = 0
        self.GIATRI = 0.0
        self.HANG = 0
