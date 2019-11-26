# -*- coding: utf-8 -*-
from snapmgr.api.cronjob import Cronjobs
from snapmgr.api.hello import Hello
from snapmgr.api.volume_snapshot_job import SnapshotPeriodicCleaningJob, VolumeSnapshotJob
from snapmgr import flask_api


resources = {
    '/hello/': Hello,
    '/cronjobs/': Cronjobs,
    '/snapshots_create_job/': VolumeSnapshotJob,  # 定时创建快照
    '/snapshots_clean_job/': SnapshotPeriodicCleaningJob,  # 定期清理快照
}


for url, viewset in resources.items():
    flask_api.add_resource(viewset, url)
