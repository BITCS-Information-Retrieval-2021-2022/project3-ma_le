from pyspark.sql import SparkSession
from operator import add
import json
import os

os.environ['JAVA_HOME'] = '/home/project/java/jdk1.8'

spark = SparkSession.builder.master("local[8]")\
    .appName("PaperRank").getOrCreate()
sc = spark.sparkContext


def parse_paper_info(paper_info_str):
    tmp = json.loads(paper_info_str)
    return tmp['Sid'], tmp['outCitations']


def get_all_paper(paper_str):
    paper_lst = [paper_str[0]]
    paper_lst.extend(paper_str[1])
    return paper_lst


# 计算本paper对引用的paper的得分贡献值
def cal_paper_contrib(paper_outCits_rank):
    outCitations = paper_outCits_rank[1][0]  # paper's OutCitations
    rank = 0 if paper_outCits_rank[1][1] is None \
        else paper_outCits_rank[1][1]  # paper's current rank
    num_outCitations = len(outCitations)
    if num_outCitations > 0:
        for outCitation in outCitations:
            yield (outCitation, rank / num_outCitations)
    else:
        yield ('dangling_paper', rank)


def update_paper_rank(paper_oldRank_rank):
    paper = paper_oldRank_rank[0]  # paper's Sid
    rank = 0 if paper_oldRank_rank[1][1] is None else paper_oldRank_rank[1][1]
    new_rank = \
        damping_factor * rank \
        + (1.0 - damping_factor) \
        + damping_factor * dangling_rank / paper_count
    return (paper, new_rank)


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
            os.rmdir(c_path)
        else:
            os.remove(c_path)


damping_factor = 0.85  # 阻尼系数
max_iterations = 5  # 迭代次数
dangling_rank = 0  # 悬挂论文的rank
paper_count = 0  # paper数量
if os.path.exists('./paper_rank_result/'):
    del_file('./paper_rank_result/')

file_list = os.listdir('Project3_citation/')
file_list = list(map(lambda x: 'Project3_citation/' + x, file_list))
file_count = len(file_list)
cnt = 0
for file in file_list:
    cnt += 1
    print("==>Processing file {0} ==>[{1}/{2}]".format(file, cnt, file_count))
    paper_list_str = sc.textFile(file, 1).cache()
    paper_outCitations = paper_list_str.map(parse_paper_info).cache()
    vertices = paper_outCitations.flatMap(get_all_paper).distinct().cache()
    paper_count = vertices.count()
    ranks = vertices.map(lambda x: (x, 1.0))
    for iteration in range(max_iterations):
        print(">>>Iteration {0}: ".format(iteration + 1))
        contrib = paper_outCitations.leftOuterJoin(ranks).\
            flatMap(cal_paper_contrib).reduceByKey(add)
        dangling_rank_lst = \
            contrib.filter(lambda x: x[0] == 'dangling_paper').collect()
        if len(dangling_rank_lst) > 0:
            dangling_rank = dangling_rank_lst[0][1]
        else:
            dangling_rank = 0
        ranks = ranks.leftOuterJoin(contrib).map(update_paper_rank)
    file_name = file.split('/')[-1]
    file_name = file_name.split('.')[0]
    ranks.coalesce(1, True).\
        saveAsTextFile('paper_rank_result/{0}'.format(file_name))
    paper_list_str.unpersist()
    paper_outCitations.unpersist()
    vertices.unpersist()
