FROM rabbitmq:management

ENV TZ=Asia/Shanghai

ENV RABBITMQ_DEFAULT_USER=admin 
ENV RABBITMQ_DEFAULT_PASS=admin 
# RUN rabbitmqctl add_user guest guest \
# && rabbitmqctl set_user_tags guest administrator \
# && rabbitmqctl  set_permissions -p "/" guest '.*' '.*' '.*'


# RUN netstat -ano | grep 5672
# RUN rabbitmqctl  set_permissions -p "/" admin '.*' '.*' '.*'

EXPOSE 15672
EXPOSE 5672
EXPOSE 4369