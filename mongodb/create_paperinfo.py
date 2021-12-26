import pymongo
from pathlib import Path
import json
import random


class Paper_Info():

    def __init__(self, paper_folder='Project3_citation', db='info',
                 collection='paper_info', start=1, end=6000, flag_init=1):
        self.paper_folder = Path(paper_folder)
        self.db = db
        self.collection = collection
        self.start = start
        self.end = end
        self.flag = flag_init
        self.cilent, self.db, self.col = self.connect_db()

    def connect_db(self):
        cilent = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cilent[self.db]
        col = db[self.collection]
        # 对集合进行初始化
        if self.flag == 1:
            if self.collection in db.list_collection_names():
                col.drop()

        return cilent, db, col

    def main(self):
        for index in range(self.start, self.end):
            file = self.paper_folder / f'citationLine{index}.jsonl'
            with open(file, 'r') as f:
                datas = f.readlines()
                datas = list(map(lambda x: json.loads(x), datas))
                for data in datas:
                    data['score'] = random.random()
                    data['_id'] = data['Sid']
                res = self.col.insert_many(datas)
                print(f'>>>{index:04}/5999\t{file}'
                      f'成功插入{len(res.inserted_ids)}条数据')
        print('>>>\t所有jsonl文件处理完毕')


if __name__ == '__main__':
    start = eval(input('请输入开始数：'))
    end = eval(input('请输入结束数：'))
    flag_init = eval(input('是否进行初始化：'))
    paper_info = Paper_Info(start=start, end=end, flag_init=flag_init)
    paper_info.main()
