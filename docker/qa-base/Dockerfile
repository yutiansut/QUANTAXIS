FROM python:3.6.5-jessie

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /requirements.txt
# for mirrors in China
# COPY pip.conf /root/.pip/pip.conf
# COPY source.list /etc/apt/sources.list

RUN apt-get update \
  && apt-get install -y apt-utils wget locales unzip \
  && locale-gen zh_CN.UTF-8 \
	&& localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
	&& echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
	&& echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
	&& echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment \
	&& curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb \
	&& dpkg -i /chrome.deb || apt-get install -yf \
	&& rm /chrome.deb \
	&& curl https://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip -o /usr/local/bin/chromedriver.zip \
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

  ENV LANG zh_CN.UTF-8
  ENV LANGUAGE zh_CN.UTF-8
  ENV LC_ALL zh_CN.UTF-8
