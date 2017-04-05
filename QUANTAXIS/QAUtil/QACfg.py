import os  
  
import ConfigParser  
  

  
def QA_util_cfg_initial(CONFIG_FILE):  

    if os.path.exists( os.path.join( os.getcwd(),CONFIG_FILE ) ):  

        config = ConfigParser.ConfigParser()  

        config.read(CONFIG_FILE)  

        #第一个参数指定要读取的段名，第二个是要读取的选项名  

        host = config.get("DB_Config", "DATABASE_HOST")   

        port = config.get("DB_Config", "DATABASE_PORT")  

        engine = config.get("DATA", "DATA_ENGINE")  

        QA_initial_setting=[str(host),str(port),str(engine)]
        return QA_initial_setting