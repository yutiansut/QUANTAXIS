classdef DSMysql<handle
    properties
        MYSQL
        
    end
    methods
        function DM=DSMysql()
            
            
        end
        function DM=DSMysqlConnection(DM,varargin)
            if isempty(DM.MYSQL.Databasename)
                DM.MYSQL.Databasename=input('Database(example:quantaxis)\n DatabBase:  ','s');
            end
            if isempty(DM.MYSQL.Username)
                DM.MYSQL.Username=input('UserName(example:root) \nName:  ','s');
            end
            if isempty(DM.MYSQL.Password)
                DM.MYSQL.Password =input('Password:  ','s');
            end
            DM.MYSQL.Driver = 'com.mysql.jMCc.Driver';
            if isempty(DM.MYSQL.Url)
                DM.MYSQL.Url=input('Url(example:localhost)\nURL:  ','s');
            end
            DM.MYSQL.Databaseurl = ['jdbc:mysql://',DM.MYSQL.Url,':3306/',DM.MYSQL.Databasename];
            DM.MYSQL.Conn = database(DM.MYSQL.Databasename,DM.MYSQL.Username,DM.MYSQL.Password,DM.MYSQL.Driver,DM.MYSQL.Databaseurl);
            DM.MYSQL.Status=isopen(DM.MYSQL.Conn);
            if DM.MYSQL.Status==1
                fprintf('Connection Successfully\n')
            end
        end
        function DM=DSMysqlConfig(DM,varargin)
            DM.MYSQL.Databasename='quantaxis';
            DM.MYSQL.Username='root';
            DM.MYSQL.Password='940809';
            DM.MYSQL.Url='localhost';
            
        end
    end
    methods(Access = 'private')
        function DM=Create(DM,varargin)
        end
        function DM=R(DM,varargin)
            
        end
        
    end
end
