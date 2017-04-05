# coding:utf-8

# -* - coding: UTF-8 -* -  
import os  
import ConfigParser  
  
CONFIG_FILE = "Config.cfg"  
  
host = "127.0.0.1"  
  
port = "27017"  
  
Data_engine='wind'

if __name__ == "__main__":  
  
         conf = ConfigParser.ConfigParser()  
  
         cfgfile = open(CONFIG_FILE,'w')  
  
         conf.add_section("DB_Config") # 在配置文件中增加一个段  
  
         # 第一个参数是段名，第二个参数是选项名，第三个参数是选项对应的值  
  
         conf.set("DB_Config", "DATABASE_HOST", host)   
  
         conf.set("DB_Config", "DATABASE_PORT", port)  
  
         conf.set("DATA", "DATA_ENGINE", Data_engine)  
  
  
         conf.add_section("FL_Config")  
  
         # 将conf对象中的数据写入到文件中  
  
         conf.write(cfgfile)  
  
         cfgfile.close()  