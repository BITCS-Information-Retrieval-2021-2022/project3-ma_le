# Project3: 基于引文网络的论文检索引擎
 
##  说明

整个项目部署在服务器中 IP地址10.108.14.126<br>
项目在服务器中的路径为 /home/project/xinxi<br>
MongoDB 版本5.0.1<br>
ElasticSearch 版本7.14.2<br>
Python 版本3.8.8<br>
<br>
#### 数据处理模块<br>
引文网络的论文重要性分数计算基于Google的PageRank算法。把每一篇论文抽象成一个节点，论文与论文之间的引用关系则是一条有向边，于是引文网络中数量庞大的论文和它们之间的相互引用关系就组成了一个巨大的有向图。<br>
如图所示，论文A和论文B都引用了论文C。在计算论文的重要性分数时，论文C的重要性分数会因为论文A和论文B对其的引用而变得更高。一篇论文的重要性分数的高低，取决于引用它的论文数量，和这些引文本身的重要性分数的高低。<br>
![image](https://user-images.githubusercontent.com/87794598/147400365-640a97b2-f84b-4176-834d-a0aa5aaf8254.png)<br>
对于引文网络中中的每一个节点，若它的重要性分数用PR值来表示，则有：
![image](https://user-images.githubusercontent.com/87794598/147400388-4768464e-d3e0-408e-8c82-b300d9edb0cf.png)<br>
表达式中各符号的含义如下：<br>
u：一篇论文<br>
Bu：引用论文u的论文的集合<br>
Nv：论文v引用的论文数量<br>
c：常数<br>
从这个公式可以看出，一篇论文本身的PR值被均匀地传递到了它引用的论文，而一篇论文最终的PR值则是引用它的论文传递过来的PR值的和。<br>
我们采用迭代算法来计算每个节点的PR值。首先为所有节点赋予一个初识的PR值，然后使用上述公式来对每一个节点的PR值进行更新，直至PR值收敛。<br>
在实际计算时，我们还引入了一个被称为“阻尼系数”的数值d，其作用是为了表达用户在浏览论文时，仍有一定的概率随机选择引文网络中的任意一篇论文，而不是完完全全的按照论文的相互引用关系进行浏览。我们将d的值取为0.85。<br>



#### 检索模块<br>



## 项目目录结构

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

##  Python依赖库
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

