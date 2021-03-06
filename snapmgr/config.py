# -*- coding: utf-8 -*-
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


environs = os.environ
mysql_host = environs['mysql_host'].strip() if environs.get('mysql_host') else '127.0.0.1'
mysql_name = environs['mysql_name'].strip() if environs.get('mysql_name') else 'cmpvirtmgr'
mysql_user = environs['mysql_user'].strip() if environs.get('mysql_user') else 'cmpvirtmgr'
mysql_password = environs['mysql_password'].strip() if environs.get('mysql_password') else 'cmpvirtmgr123'
mysql_port = environs['mysql_port'].strip() if environs.get('mysql_port') else '3306'


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

    # cinder client configuration
    AUTH_URL = environs['auth_url'].strip() if environs.get('auth_url') else "http://172.31.11.204:5000/v2.0"
    AUTH_VERSION = environs['auth_version'].strip() if environs.get('auth_version') else "3"
    USERNAME = environs['username'].strip() if environs.get('username') else "admin"
    PASSWORD = environs['password'].strip() if environs.get('password') else "admin"
    TENANT_NAME = environs['tenant_name'].strip() if environs.get('tenant_name') else "admin"
    REGION_NAME = environs['region_name'].strip() if environs.get('region_name') else "RegionOne"

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
