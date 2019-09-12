FROM daocloud.io/quantaxis/qabase:latest

COPY daily_update /etc/cron.d/daily_update
COPY entrypoint.sh /entrypoint.sh

WORKDIR home

RUN apt-get update \
	&& apt-get install -y cron --allow-unauthenticated\
	&& chmod 0644 /etc/cron.d/daily_update \
	&& chmod +x /QUANTAXIS/config/update_all.py \
	&& crontab /etc/cron.d/daily_update \
	&& chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["cron", "-f"]
