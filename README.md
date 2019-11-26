---
一个基于Web Flask框架的定时创建Openstack集群卷快照和定期清理卷快照的项目，
主要用到Flask知识点包括：
* flask sqlalchemy
* flask restful
* flask APscheduler
* flask blueprint

## 运行

```bash
cd snapmgr
source env/bin/activate
python runserver.py
```