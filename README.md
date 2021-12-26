# Project3: 基于引文网络的论文检索引擎
 
##  说明

整个项目部署在服务器中 IP地址10.108.14.126<br>
项目在服务器中的路径为 /home/project/xinxi<br>
MongoDB 版本5.0.1<br>
ElasticSearch 版本7.14.2<br>
#### 项目目录结构

├── mongodb 数据库相关代码<br>
│   ├── create_paperinfo.py   生成基础的信息<br>
│   ├── crearte_score.py      整合分数生成json<br>
│   ├── info_score.py         将分数插入mongodb<br>
│   ├── paper_rank.py         计算重要性分数<br>
├── project3              Django后端代码<br>
│   ├── function.py           功能实现<br>
├── web                   打包的前端<br>
├── manage.py             Django框架<br>
└── infosearch.zip        前端代码<br>

##  依赖的三方库
Django                  3.2.9<br>
django-cors-headers     3.10.1<br>
elastic2-doc-manager    1.0.0<br>
elasticsearch           7.14.2<br>
mongo-connector         3.1.1<br>

##  运行项目
启动ElasticSearch：<br>

    ~/ElasticSearch/elasticsearch-7.14.2/bin$ ./elasticsearch

启动Django：<br>

    ~/project3$ python manage.py runserver 0:8000

启动Nginx：<br>

    sudo service nginx start

#### 访问服务器：http://10.108.14.126/

##  配置
启动MongoDB

    sudo systemctl start mongodb.service
    
启动ElasticSearch
    
    ~/ElasticSearch/elasticsearch-7.14.2/bin$ ./elasticsearch
      
如果MongoDB中数据有变化则需要进行数据同步<br>
    
    mongo-connector -m localhost:27017 -t localhost:9200 -d elastic2_doc_manager
    
启动Nginx<br>

    sudo service nginx start

Nginx的下载与配置可见：https://blog.csdn.net/lgno2/article/details/111148770<br>

