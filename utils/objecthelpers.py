
from typing import TypeVar, Generic
T = TypeVar('T')


class helper:
    @staticmethod
    def toObject(cols,row, obj):
        for key in cols.keys():
            if hasattr(obj,key):
                #print("key {} : value : {}".format(key,row[cols[key]]))
                setattr(obj,key,row[cols[key]])
            else:
                if hasattr(obj,key.upper()):
                    setattr(obj, key.upper(), row[cols[key]])

    @staticmethod
    def toList(results,obj):
        pass
        
