FROM nvidia/cuda:10.2-runtime-ubuntu18.04

COPY setup.sh /root/setup.sh

RUN cd ~ && chmod u+x setup.sh && ./setup.sh && rm -rfv setup.sh

CMD ["bash", "/entrypoint.sh"]
