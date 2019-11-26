# -*- coding: utf-8 -*-
"""
实现定时创建卷快照和定期删除卷快照逻辑
"""
import time
import uuid

from apscheduler.triggers.cron import CronTrigger
from flask import request
from flask_restful import Resource

from snapmgr import scheduler
from snapmgr.libs.utils import clean_volume_snapshot, create_volume_snapshot


class VolumeSnapshotJob(Resource):

    def post(self):
        volume_id = request.get_json()['volume_id']
        job_name = 'snapshot_create_for_volume_%s' % volume_id
        cron_trigger = request.get_json()['cron_trigger']
        snapshot_name = request.get_json()['snapshot_name']
        snapshot_created_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
        snapshot_name = snapshot_name + '_' + snapshot_created_time
        scheduler.add_job(func=create_volume_snapshot, args=[volume_id, snapshot_name],
                          tirgger=CronTrigger.from_crontab(cron_trigger),
                          id=str(uuid.uuid4()), name=job_name, jobstore='default')
        return {'create_snapshot': 'success'}


class SnapshotPeriodicCleaningJob(Resource):

    def post(self):
        volume_id = request.get_json()['volume_id']
        job_name = 'snapshot_periodic_clean_for_volume_{}'.format(volume_id)
        expired_days = request.get_json()['expired_days']
        scheduler.add_job(func=clean_volume_snapshot, args=[volume_id, expired_days], trigger='cron',
                          second='*/60', id=str(uuid.uuid4()), name=job_name, jobstore='default')
        return {'clean_expired_snapshots': 'success'}
