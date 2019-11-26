# -*- coding: utf-8 -*-
"""
此段代码仅供测试之用，权且留下吧
"""
import os
import time
import uuid

from flask import request
from flask_restful import Resource
from apscheduler.triggers.cron import CronTrigger

from snapmgr import scheduler


def write_data_func(source_data):
    created_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    source_data = '{}: {}'.format(created_time, source_data)
    write_cmd = 'echo %s >> /tmp/test_cron.txt' % source_data
    os.system(write_cmd)


class Cronjobs(Resource):

    def get(self):
        print(scheduler.get_jobs())
        jobs = []
        for job in scheduler.get_jobs():
            jobs.append({
                "name": job.name,
                "id": job.id
            })
        return {"jobs": jobs}

    def post(self):
        print(request.get_json())
        write_data = request.get_json()['source_data']
        job_name = request.get_json()['name']

        #scheduler.add_job(
        #    func=write_data_func, args=[write_data], trigger='cron',
        #    second='*/10', id=str(uuid.uuid4()), name=job_name, jobstore='default')
        scheduler.add_job(
            func=write_data_func, args=[write_data], trigger=CronTrigger.from_crontab('*/2 * * * *'),
            id=str(uuid.uuid4()), name=job_name, jobstore='default')
        return 'ok'
