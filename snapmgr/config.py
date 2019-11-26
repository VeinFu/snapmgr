# -*- coding: utf-8 -*-
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


environs = os.environ
mysql_host = environs['mysql_host'] if environs.get('mysql_host') else '127.0.0.1'
mysql_name = environs['mysql_name'] if environs.get('mysql_name') else 'cmpvirtmgr'
mysql_user = environs['mysql_user'] if environs.get('mysql_user') else 'cmpvirtmgr'
mysql_password = environs['mysql_password'] if environs.get('mysql_password') else 'cmpvirtmgr123'
mysql_port = environs['mysql_port'] if environs.get('mysql_port') else '3306'


def _mysql_config(host, name, user, password, port):
    return 'mysql://{user}:{password}@{host}:{port}/{name}?charset=utf8'.format(
        user=user, password=password, host=host, port=port, name=name)


class BasicConfig(object):

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = _mysql_config(
        host=mysql_host,
        name=mysql_name,
        user=mysql_user,
        password=mysql_password,
        port=mysql_port
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTFUL_JSON = {'ensure_ascii': False}


class DevelopmentConfig(BasicConfig):

    DEBUG = True

    SCHEDULER_API_ENABLED = True
    SCHEDULER_API_PREFIX = '/snapmgr_api'

    LIBVIRT_KEEPALIVE_INTERVAL = 5
    LIBVIRT_KEEPALIVE_COUNT = 5

    # cinder client configuration
    AUTH_URL = environs['auth_url'] if environs.get('auth_url') else "http://172.31.11.204:5000/v2.0"
    AUTH_VERSION = environs['auth_version'] if environs.get('auth_version') else "2"
    USERNAME = environs['username'] if environs.get('username') else "admin"
    PASSWORD = environs['password'] if environs.get('password') else "admin"
    TENANT_NAME = environs['tenant_name'] if environs.get('tenant_name') else "admin"
    REGION_NAME = environs['region_name'] if environs.get('region_name') else "RegionOne"

    # 定时任务持久化设置
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=_mysql_config(
            host=mysql_host,
            name=mysql_name,
            user=mysql_user,
            password=mysql_password,
            port=mysql_port
        ))
    }
