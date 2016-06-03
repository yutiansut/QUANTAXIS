classdef DSMysql<handle
    properties
        MYSQL
        
    end
    methods
        function DM=DSMysql()
            DM.DSMysqlInit();
            
        end
        function DM=DSMysqlInit(DM)
            DM.MYSQL.DatabaseName=[];
            DM.MYSQL.TableName=[];
            DM.MYSQL.Describe=[];
            DM.MYSQL.User=[];
            DM.MYSQL.Password=[];
            DM.MYSQL.Url=[];
            DM.MYSQL.Driver = 'com.mysql.jMCc.Driver';
        end
        function DM=DSMysqlConnect(DM,varargin)
            if isempty(DM.MYSQL.DatabaseName)
                DM.MYSQL.DatabaseName=input('Database(example:quantaxis)\n DatabBase:  ','s');
            end
            if isempty(DM.MYSQL.User)
                DM.MYSQL.User=input('User(example:root) \nName:  ','s');
            end
            if isempty(DM.MYSQL.Password)
                DM.MYSQL.Password =input('Password:  ','s');
            end
            DM.MYSQL.Driver = 'com.mysql.jMCc.Driver';
            if isempty(DM.MYSQL.Url)
                DM.MYSQL.Url=input('Url(example:localhost)\nURL:  ','s');
            end
            DM.MYSQL.Databaseurl = ['jdbc:mysql://',DM.MYSQL.Url,':3306/',DM.MYSQL.DatabaseName];
            DM.MYSQL.Conn = database(DM.MYSQL.DatabaseName,DM.MYSQL.User,DM.MYSQL.Password,DM.MYSQL.Driver,DM.MYSQL.Databaseurl);
            DM.MYSQL.Status=isopen(DM.MYSQL.Conn);
            if DM.MYSQL.Status==1
                fprintf('Connection Successfully\n')
            end
        end
        function DM=DSMysqlConfig(DM,varargin)
            DM.MYSQL.DatabaseName='quantaxis';
            DM.MYSQL.User='root';
            DM.MYSQL.Password='940809';
            DM.MYSQL.Url='localhost';
            
        end
    end
    methods(Access = 'public')
        function DM=CreateTable(DM,varargin)
            if isempty(DM.MYSQL.DatabaseName)
                DM.MYSQL.DatabaseName=input('Database(example:quantaxis)\n DatabBase:  ','s');
            end
            if isempty(DM.MYSQL.TableName)
                DM.MYSQL.TableName=input('TableName(example:000001_ts) \nName:  ','s');
            end
            if isempty(DM.MYSQL.Describe)
                DM.MYSQL.Describe =input('Describe(example:(`DATE`DOUBLE NULL)) \nName','s');
            end
            DM.MYSQL.Sqlquery=['CREATE TABLE if not exists `',DM.MYSQL.DatabaseName,'`.`',DM.MYSQL.TableName,'` ', DM.MYSQL.Describe,';'];
            disp(DM.MYSQL.Sqlquery);
            exec(DM.MYSQL.Conn,DM.MYSQL.Sqlquery);
            %CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name [(create_definition,...)][table_options] [select_statement]
            
        end
        function DM=R(DM,varargin)
            
        end
        
    end
end
