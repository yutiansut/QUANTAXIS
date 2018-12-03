FROM python:3.6.5-jessie

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /requirements.txt
# COPY pip.conf /root/.pip/pip.conf
# COPY source.list /etc/apt/sources.list

RUN apt-get update \
  && apt-get install -y apt-utils \
  && apt-get install -y wget \
	&& curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb \
	&& dpkg -i /chrome.deb || apt-get install -yf \
	&& rm /chrome.deb \
	&& curl https://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip -o /usr/local/bin/chromedriver.zip \
	&& apt-get install unzip \
	&& unzip /usr/local/bin/chromedriver.zip \
	&& mv /chromedriver /usr/local/bin/ \
	&& rm /usr/local/bin/chromedriver.zip \
	&& chmod +x /usr/local/bin/chromedriver \
  && git clone https://github.com/QUANTAXIS/QUANTAXIS \
  && cd QUANTAXIS \
  && pip install -r /QUANTAXIS/requirements.txt \
  && pip install -r /requirements.txt \
  && pip install -e . \
	&& apt-get clean -y \
	&& apt-get autoclean -y \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
