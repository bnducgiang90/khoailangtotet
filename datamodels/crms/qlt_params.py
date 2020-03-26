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
    pass

class QLT_PARAMS_HSDN_DGTC:
    pass

class QLT_PARAMS_HSDN_PLDCC:
    pass

class QLT_PARAMS_HSDN_PTAD:
    pass

class QLT_PARAMS_HSDN_TC_MOTA:
    pass

####Thong tin các bảng params HSVP:
class QLT_PARAMS_HSVP_HSPLTN:
    pass

class QLT_PARAMS_HSVP_HSPLXNK:
    pass

class QLT_PARAMS_HSVP_PLCLT:
    pass

class QLT_PARAMS_HSVP_PLHSVP:
    pass

class QLT_PARAMS_HSVP_PLSLVP:
    pass

class QLT_PARAMS_HSVP_PLTLVP:
    pass

class QLT_PARAMS_HSVP_PLVP:
    pass

class QLT_PARAMS_HSVP_PLVPKTK:
    pass

## thông tin bảng params QLT_PARAMS_PLXEPHANG
class QLT_PARAMS_PLXEPHANG:
    pass
