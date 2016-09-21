# Ansible Rest API 
Tornado project for  Ansible Rest API service.


## 安装

### 安装依赖包

1. 采用ansible api 1.0
    
    pip install -r requirements-v1.txt
    
2. 采用ansible api 2.0
    
    pip install -r requirements-v2.txt

### 启动Celery

1. 采用ansible api 1.0
  
    cd ansible-api                     
    celery worker --app=celerytask.celeryapp.app -l info  -c 1
    
2. 采用ansible api 2.0

    cd ansible-api
    export PYTHONOPTIMIZE=1                                   
    celery worker --app=celerytask.celeryapp.app -l info  -c 1
