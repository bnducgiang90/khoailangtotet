import yaml

class filehelper:

    @staticmethod
    def readfile(filepath: str):
        with open(filepath, 'r') as reader:
           str = reader.readlines()
        
        return str

    @staticmethod
    def savefile(filepath: str):
        pass

    @staticmethod
    def readyalmfile(filepath: str):
        with open(filepath,'r') as file:
            result = yaml.load(file, Loader=yaml.FullLoader)
        return result
