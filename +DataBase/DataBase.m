classdef DataBase<handle
    properties
        MYSQL
        
    end
    methods
        function DB=DataBase()
            
            
        end
        function DB=MySQL(DB,varargin)
            DB.MYSQL.Databasename=input('Database(example:quantaxis)\n DatabBase:  ','s');
            DB.MYSQL.Username=input('UserName(example:root) \nName:  ','s');
            DB.MYSQL.Password =input('Password:  ','s');
            DB.MYSQL.Driver = 'com.mysql.jdbc.Driver';
            DB.MYSQL.Url=input('Url(example:localhost)\nURL:  ','s');
            DB.MYSQL.Databaseurl = ['jdbc:mysql://',DB.MYSQL.Url,':3306/',DB.MYSQL.Databasename];
            DB.MYSQL.Conn = database(DB.MYSQL.Databasename,DB.MYSQL.Username,DB.MYSQL.Password,DB.MYSQL.Driver,DB.MYSQL.Databaseurl);
            DB.MYSQL.Status=isopen(DB.MYSQL.Conn);
            if DB.MYSQL.Status==1
                fprintf('Connection Successfully')
            end
        end
    end
    methods(Access = 'private')
        function DB=Create(DB,varargin)
        end
        function DB=R(DB,varargin)
            
        end
        
    end
end
