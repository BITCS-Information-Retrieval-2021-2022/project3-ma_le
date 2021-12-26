import random
import time

from elasticsearch import Elasticsearch


def random_score(cnt):  # 由于ES检索中分数是完全随机生成的 故此根据被引用数重新随机生成一次
    if cnt == 0:
        return random.uniform(0.0, 0.25)
    elif cnt <= 3:  # 1-3
        return random.uniform(0.25, 0.5)
    elif cnt <= 5:  # 4-5
        return random.uniform(0.5, 0.75)
    else:
        return random.uniform(0.75, 1.0)


def fuzz_search(value):
    es = Elasticsearch()
    body = {
        "query": {
            "match": {
                "title": {
                    "query": value,
                    "fuzziness": "AUTO",
                    "operator": "and"
                }
            }
        }
    }
    res = es.search(index="info_retrieval",
                    doc_type="test_paper_info",
                    body=body,
                    request_timeout=30)
    res_list = []
    for hit in res['hits']['hits']:
        res_list.append(hit['_source'])
    for paper in res_list:
        paper['score'] = random_score(paper['inCitationsCount'])

    sorted_list = sorted(res_list,
                         key=lambda x: x.__getitem__('score'),
                         reverse=True)

    return res_list, sorted_list


def search_by_sid(value):
    # return a single paper
    # return a dict with values if exist
    # else return a empty dict
    es = Elasticsearch()
    body = {
        "query": {
            "term": {
                "Sid": value
            }
        }
    }
    res = es.search(index="info_retrieval",
                    doc_type="test_paper_info",
                    body=body)
    res_dict = {}
    if res['hits']['total']['value'] != 0:
        res_dict = res['hits']['hits'][0]['_source']

    return res_dict


def draw(value):
    def write(s):
        filename = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        with open(filename, 'w') as f:
            f.write(s)

    def search(id):
        res_dict = search_by_sid(id)
        if len(res_dict) == 0:
            res_dict['Sid'] = id
            res_dict['title'] = ''
            res_dict['year'] = ''
            res_dict['inCitations'] = []
            res_dict['outCitations'] = []
            res_dict['inCitationsCount'] = 0
            res_dict['outCitationsCount'] = 0
            res_dict['score'] = 0
        return res_dict

    res_dict = search(value)
    id_set = set()
    id_set.add(value)
    papers_list = [res_dict]
    for id in res_dict['outCitations']:  # 一级引用
        id_set.add(id)
        tmp_res = search(id)
        papers_list.append(tmp_res)
        # for _id in tmp_res['outCitations']:  # 二级引用
        #     if _id not in id_set:
        #         id_set.add(_id)
        #         _tmp_res = search(_id)
        #         papers_list.append(_tmp_res)
        for _id in tmp_res['inCitations']:
            if _id not in id_set:
                id_set.add(_id)
                _tmp_res = search(_id)
                papers_list.append(_tmp_res)
    for id in res_dict['inCitations']:
        id_set.add(id)
        tmp_res = search(id)
        papers_list.append(tmp_res)
        for _id in tmp_res['outCitations']:
            if _id not in id_set:
                id_set.add(_id)
                _tmp_res = search(_id)
                papers_list.append(_tmp_res)
        # for _id in tmp_res['inCitations']:
        #     if _id not in id_set:
        #         id_set.add(_id)
        #         _tmp_res = search(_id)
        #         papers_list.append(_tmp_res)
    nodes_dict = {}
    i = 0
    for id in id_set:
        nodes_dict[id] = i
        i += 1
    nodes = []
    edges = []
    max_in = max_out = 0
    for id in id_set:
        for paper in papers_list:
            if paper['Sid'] == id:
                if max_in < paper['inCitationsCount']:
                    max_in = paper['inCitationsCount']
                if max_out < paper['outCitationsCount']:
                    max_out = paper['outCitationsCount']
                paper['score'] = random_score(paper['inCitationsCount'])
                if paper['score'] < 0.25:
                    _class = "c3"
                elif paper['score'] < 0.5:
                    _class = "c2"
                elif paper['score'] < 0.75:
                    _class = "c1"
                elif paper['score'] <= 1:
                    _class = "c0"
                x = random.randint(-500, 1500)
                y = random.randint(-500, 1500)
                nodes.append({"id": str(nodes_dict[id] + 1),
                              "label": str(nodes_dict[id] + 1),
                              "title": paper['title'],
                              "year": paper['year'],
                              'score': paper['score'],
                              "class": _class,
                              "x": x,
                              "y": y
                              })
    edges_set = set()
    for paper in papers_list:
        node_1 = nodes_dict[paper['Sid']]
        for _id in paper['outCitations']:
            if _id in id_set:
                node_2 = nodes_dict[_id]
                edges_set.add((node_1, node_2))
        for _id in paper['inCitations']:
            if _id in id_set:
                node_2 = nodes_dict[_id]
                edges_set.add((node_2, node_1))
    for x in edges_set:
        edges.append({'source': str(x[0] + 1), 'target': str(x[1] + 1)})
    res = {'nodes': nodes, 'edges': edges}

    s = "-----Statistics-----" \
        + "\npaper id:  " + str(value) \
        + "\nnum of nodes:  " + str(len(nodes)) \
        + "\nnum of edges:  " + str(len(edges)) \
        + "\nmax in:  " + str(max_in) \
        + "\nmax out:  " + str(max_out)
    write(s)

    return res
