FROM barretthugh/qa-base

COPY entrypoint.sh /entrypoint.sh

WORKDIR home

RUN pip install git+https://github.com/yutiansut/tornado_http2 \
	&& pip install quantaxis_webserver \
	&& chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8010

CMD ["quantaxis_webserver", "--port=8010", "&"]
