import os
import configparser
rootdir = os.path.abspath("")
config_path = os.path.join(rootdir, 'configuration.conf')
config_path_ini = os.path.join(rootdir, 'properties.ini')
config = configparser.ConfigParser()
config.read(config_path_ini)

class oracleconfig:
      hostname = config["oracle"]["hostname"]
      username = config["oracle"]["username"]
      password = config["oracle"]["password"]

class postgresconfig:
      host = config["postgresql"]["host"]
      user = config["postgresql"]["user"]
      passwd = config["postgresql"]["passwd"]
      db = config["postgresql"]["db"]

class mysqlconfig:
      host = config["mysql"]["host"]
      user = config["mysql"]["user"]
      passwd = config["mysql"]["passwd"]
      db = config["mysql"]["db"]

class logconfig:
      pathfile = config["logging"]["path"]
      logconfigfile  = config["logging"]["logconfigfile"]

# username = "CRMS"
# password = "Oracle123"
# hostname = "10.15.68.159:1521/FRAUDB"
settings = {}
class configutils:

    @staticmethod
    def getsettings():
      if(not settings):
        print("config:", config_path)
        try:
          with open(config_path, 'r') as reader:
            for line in reader.readlines():
              line = line.rstrip('\n')
            #while line != '':  # The EOF char is an empty string
              print(line, end='')
              if line.startswith("#"):
                continue
              keyvalue = line.split("=")
              if keyvalue[0].strip() in settings :
                continue
              else:
                settings.update({keyvalue[0].strip() : keyvalue[1].strip()})
          return settings   
        except IOError as ex:
          print(ex)

      return settings
    