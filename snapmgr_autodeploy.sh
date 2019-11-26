#!/bin/sh

docker_env=0
ifconfig br-mgmt > /dev/null
if [ $? -ne 0 ];then
	docker_env=1
fi

if [ $docker_env -eq 0 ];then
	mgmt_addr=$(ifconfig br-mgmt | awk '/inet addr/ {print$2}' | awk -F \: '{print $2}')
fi

# 拷贝supervisor项目进程文件并更新配置
cp /var/www/snapmgr/conf/supervisor/* /etc/supervisor/conf.d/

# gunicorn配置更新
if [ $docker_env -eq 0 ];then
	sed -i 's/127.0.0.1/'$mgmt_addr'/g' /etc/supervisor/conf.d/gunicorn.conf
fi

# nginx配置
cp /var/www/snapmgr/conf/nginx/default /etc/nginx/sites-available/
if [ $docker_env -eq 0 ];then
	sed -i 's/127.0.0.1/'$mgmt_addr'/g' /etc/nginx/sites-available/default
fi
rm -fr /etc/nginx/sites-enabled/*
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
sed -i '/user www-data/d' /etc/nginx/nginx.conf
sed -i '/worker_processes/'d /etc/nginx/nginx.conf
sed -i '1i user root;\nworker_processes 1;\ndaemon off;' /etc/nginx/nginx.conf
