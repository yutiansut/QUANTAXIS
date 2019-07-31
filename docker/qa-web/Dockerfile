FROM yutiansut/qabase:latest

COPY entrypoint.sh /entrypoint.sh

WORKDIR home

RUN pip install git+https://github.com/yutiansut/tornado_http2 \
	&& pip install quantaxis_webserver \
	&& pip install tornado==5.1.0 \
	&& chmod +x /entrypoint.sh \
	&& chmod +x /QUANTAXIS/QUANTAXIS/QAUtil/QASetting.py



EXPOSE 8010

CMD ["bash", "/entrypoint.sh"]
