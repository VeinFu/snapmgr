---
一个基于Web Flask框架的定时创建Openstack集群卷快照和定期清理卷快照的项目，
主要用到Flask知识点包括：
* flask sqlalchemy
* flask restful
* flask APscheduler
* flask blueprint

## 容器化部署

### 1. 下载源码
```bash
git clone git@github.com:VeinFu/snapmgr.git
```

### 2. 源码打包

```bash
tar zcvf snapmgr.tar.gz snapmgr
```

### 3. 构建Docker镜像
```bash
mkdir -p $HOME/build
cp snapmgr.tar.gz $HOME/build
cp snapmgr/Dockerfile $HOME/build
cd $HOME/build
docker build -t snapmgr -f .
```

### 4. 创建配置文件
touch $HOME/snapmgr.conf

文件内容可参照如下（视实际环境配置）：
```bash
# mysql config
mysql_host=192.168.0.2
mysql_user=snapmgr
mysql_name=snapmgr
mysql_password=snapmgr123
mysql_port=3306

# openstack auth
auth_url=http://192.168.0.9:5000/v2.0
auth_version=2
username=admin
password=admin
tenant_name=admin
region_name=RegionOne
```

### 5. 运行
```bash
docker run -d --name test_snapmgr --network=host --restart=always --env-file=$H
OME/snapmgr.conf snapmgr
```