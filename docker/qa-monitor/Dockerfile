FROM nicolargo/glances
ENV GLANCES_OPT="-w"
COPY glances.conf /glances/conf/glances.conf
CMD python -m glances -C /glances/conf/glances.conf $GLANCES_OPT
