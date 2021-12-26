# Project3: 基于引文网络的论文检索引擎
 
##  说明
**见master分支**<br>
整个项目部署在服务器中 IP地址10.108.14.126<br>
项目在服务器中的路径为 /home/project/xinxi<br>
MongoDB 版本5.0.1<br>
ElasticSearch 版本7.14.2<br>
Python 版本3.8.8<br>
<br>
#### 数据处理模块<br>
引文网络的论文重要性分数计算基于Google的PageRank算法。把每一篇论文抽象成一个节点，论文与论文之间的引用关系则是一条有向边，于是引文网络中数量庞大的论文和它们之间的相互引用关系就组成了一个巨大的有向图。<br>
如图所示，论文A和论文B都引用了论文C。在计算论文的重要性分数时，论文C的重要性分数会因为论文A和论文B对其的引用而变得更高。一篇论文的重要性分数的高低，取决于引用它的论文数量，和这些引文本身的重要性分数的高低。<br>
![image](https://user-images.githubusercontent.com/87794598/147400421-ed8ca6b8-7414-428b-83f2-a03b25ce5ddf.png)<br>
对于引文网络中中的每一个节点，若它的重要性分数用PR值来表示，则有：<br>
![image](https://user-images.githubusercontent.com/87794598/147400418-6740b464-93ff-4603-82a2-32be76845e8d.png)<br>
表达式中各符号的含义如下：<br>
u：一篇论文<br>
Bu：引用论文u的论文的集合<br>
Nv：论文v引用的论文数量<br>
c：常数<br>
<br>
从这个公式可以看出，一篇论文本身的PR值被均匀地传递到了它引用的论文，而一篇论文最终的PR值则是引用它的论文传递过来的PR值的和。<br>
我们采用迭代算法来计算每个节点的PR值。首先为所有节点赋予一个初识的PR值，然后使用上述公式来对每一个节点的PR值进行更新，直至PR值收敛。<br>
在实际计算时，我们还引入了一个被称为“阻尼系数”的数值d，其作用是为了表达用户在浏览论文时，仍有一定的概率随机选择引文网络中的任意一篇论文，而不是完完全全的按照论文的相互引用关系进行浏览。我们将d的值取为0.85。<br>
![image](https://user-images.githubusercontent.com/87794598/147400439-3e892f8d-9377-414d-aa6c-523e0877229e.png)<br>
在引文网络中，会存在一些没有出度的节点，即这些论文没有引用其他任何一篇论文，每一轮迭代计算结束之前，我们会将这些节点的PR值收集起来，平均地分配到引文网络中的所有节点。<br>
<br>
#### 检索模块&显示模块<br>
首页/搜索页：<br>
![1640501527(1)](https://user-images.githubusercontent.com/87794598/147401204-27b68562-cddb-4f92-9ce5-facd12ee6ac3.jpg)<br>
<br>
检索结果列表页：<br>
![1640501773(1)](https://user-images.githubusercontent.com/87794598/147401261-3692a8aa-2a99-4e98-a132-f7586528bff6.jpg)<br>
搜索结果最多显示10条数据<br>
可以点击切换按钮来选择显示ES基础检索结果列表或是基于引文网络重要性分数改善后的检索结果列表<br>
根据重要性分数大小来对检索结果列表进行改善<br>
点击一篇论文后可以在右侧显示出基于它的引文网络图，图中的节点包括它**自己**、**它引用的节点**、**引用了它引用的节点的节点**、**引用它的节点**以及**引用了它的节点所引用的节点**


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


## 关于前端源代码

### Project setup
```
npm install
```
### download dependency library
```
npm install axios
npm install element-ui
npm install router
```
### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```
### note
```
if you want to Deploy the project to the server,please modify the url in src/App.vue  and  src/views/About.vue(for instance /api/)  to the realistic url of your server back end interface.
```
### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


