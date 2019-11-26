FROM python3.7
MAINTAINER fuchunhui@umcloud.com
ADD ./snapmgr/* /var/www/
WORKDIR /var/www/
RUN cd snapmgr \
    && ../env/bin/pip install -r requirements.txt \
    && apt-get install -y supervisor nginx \
    && update-rc.d -f nginx remove \
    && sh snapmgr_autodeploy.sh \
    && cd .. \
    && rm -fr *.gz

CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]