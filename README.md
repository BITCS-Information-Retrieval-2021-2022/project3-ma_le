# Project3: 基于引文网络的论文检索引擎
 
##  说明

整个项目部署在服务器中 IP地址10.108.14.126<br>
项目在服务器中的路径为 /home/project/xinxi


##  运行项目
启动ElasticSearch：<br>

    ~/ElasticSearch/elasticsearch-7.14.2/bin$ ./elasticsearch

启动Django：<br>

    ~/project3$ python manage.py runserver 0:8000

启动Nginx：<br>

    sudo service nginx start


##  配置
**MongoDB**
    版本    5.0.1<br>启动：
    
    sudo systemctl start mongodb.service
    
**ElasticSearch**
版本    7.14.2<br>启动： 
    
    ~/ElasticSearch/elasticsearch-7.14.2/bin$ ./elasticsearch
      
如果MongoDB中数据有变化则需要进行数据同步：<br>
    
    mongo-connector -m localhost:27017 -t localhost:9200 -d elastic2_doc_manager


依赖的三方库               版本
Django                  3.2.9
django-cors-headers     3.10.1
elastic2-doc-manager    1.0.0
elasticsearch           7.14.2
mongo-connector         3.1.1
