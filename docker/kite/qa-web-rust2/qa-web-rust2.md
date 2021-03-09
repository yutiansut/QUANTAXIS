WEB SERVICE版镜像文件；

修改期货股票两个update文件第一行解释器路径，替换为 #!/opt/conda/bin/python；

附带web service服务中crontab进程的启动指令，拷贝到yaml文件该服务下替换原来 command:指令行

        command:
            - /bin/bash
            - -c
            - |                 
                /root/wait_for_it.sh qaeventmq:15672   
                /root/runcelery.sh &    
                cron -f 
