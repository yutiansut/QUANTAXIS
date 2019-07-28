FROM yutiansut/qabase:v156

COPY entrypoint.sh /entrypoint.sh

WORKDIR home

RUN pip install git+https://github.com/yutiansut/tornado_http2 \
	&& pip install quantaxis_webserver \
	&& pip install tornado==5.1.0 \
	&& chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8010

CMD ["quantaxis_webserver", "--port=8010", "&"]
