import decimal

##class crms_tokhai_nothue - mapping với bảng CRMS_TOKHAI_NOTHUE
class crms_tokhai_nothue:
    def __init__(self):
        ## private varibale or property in Python
        self.ID: decimal = None
        self.MA_HQXL: str = None
        self.MA_DV: str = None

    ## getter method to get the properties using an object
    def get_ID(self):
        return self.ID

    ## setter method to change the value 'a' using an object
    def set_ID(self, ID):
        self.ID = ID

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
