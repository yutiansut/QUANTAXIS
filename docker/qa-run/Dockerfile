FROM daocloud.io/quantaxis/qawebserver:latest
# RUN \ 
# apt-get clean && cd /var/lib/apt && mv lists lists.old && mkdir -p lists/partial && apt-get clean\
# && apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 40976EAF437D05B5

# RUN \
# echo 'deb http://www.rabbitmq.com/debian/ testing main' | tee /etc/apt/sources.list.d/rabbitmq.list \
# && wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | apt-key add - \
# && apt-get update -y --force-yes && apt-get install rabbitmq-server -y --force-yes \ 
# && rabbitmq-plugins enable rabbitmq_management \
# && rabbitmqctl add_user admin admin \
# && rabbitmqctl set_user_tags admin administrator \
# && rabbitmqctl  set_permissions -p "/" admin '.*' '.*' '.*'


RUN \
git clone https://github.com/yutiansut/QAPUBSUB \
&& cd QAPUBSUB && pip install -e . && cd ..\
&& git clone https://github.com/yutiansut/QUANTAXIS_RUN \
&& cd QUANTAXIS_RUN && pip install -e . && pip install eventlet

COPY runcelery.sh /root/
RUN chmod +x /root/runcelery.sh

CMD ["bash", "/root/runcelery.sh"]