classdef Mysql<handle
    properties
        MYSQL
        
    end
    methods
        function MC=DataBase()
            
            
        end
        function MC=Mysql(MC,varargin)
            MC.MYSQL.Databasename=input('Database(example:quantaxis)\n DatabBase:  ','s');
            MC.MYSQL.Username=input('UserName(example:root) \nName:  ','s');
            MC.MYSQL.Password =input('Password:  ','s');
            MC.MYSQL.Driver = 'com.mysql.jMCc.Driver';
            MC.MYSQL.Url=input('Url(example:localhost)\nURL:  ','s');
            MC.MYSQL.Databaseurl = ['jdbc:mysql://',MC.MYSQL.Url,':3306/',MC.MYSQL.Databasename];
            MC.MYSQL.Conn = database(MC.MYSQL.Databasename,MC.MYSQL.Username,MC.MYSQL.Password,MC.MYSQL.Driver,MC.MYSQL.Databaseurl);
            MC.MYSQL.Status=isopen(MC.MYSQL.Conn);
            if MC.MYSQL.Status==1
                fprintf('Connection Successfully')
            end
        end
    end
    methods(Access = 'private')
        function MC=Create(MC,varargin)
        end
        function MC=R(MC,varargin)
            
        end
        
    end
end
