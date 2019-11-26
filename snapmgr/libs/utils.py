# -*- coding: utf-8 -*-
import datetime
import time

from cinderclient import client as cinder_client

from snapmgr import app


def get_cinder_client():
    return cinder_client.Client(
        app.config['AUTH_VERSION'],
        app.config['USERNAME'],
        app.config['PASSWORD'],
        app.config['TENANT_NAME'],
        app.config['AUTH_URL'],
        region_name=app.config['REGION_NAME']
    )


def create_volume_snapshot(volume_id, snapshot_name):
    client = get_cinder_client()
    client.volume_snapshots.create(volume_id, force=True, name=snapshot_name)


def clean_volume_snapshot(volume_id, days):
    client = get_cinder_client()
    snapshots = client.volume_snapshots.list(search_opts={'volume_id': volume_id})
    for snapshot in snapshots:
        snapshot_created_date = str(snapshot.created_at)
        snapshot_created_date = snapshot_created_date.split('.')[0].replace('T', ' ')
        snapshot_created_time = datetime.datetime.strptime(snapshot_created_date, '%Y-%m-%d %H:%M:%S')
        snapshot_created_time = time.mktime(snapshot_created_time.timetuple())
        if (time.time() - snapshot_created_time) > days * 24 * 3600:
            # 删除快照接口无论该快照是否被使用创建新卷都能调用成功，不过对被使用创建新卷的快照实际上并没有删除，
            # 但这也是期望的结果，因此可忽略Openstack M版的这个bug，前端页面无需做异常处理
            client.volume_snapshots.delete(str(snapshot.id))
