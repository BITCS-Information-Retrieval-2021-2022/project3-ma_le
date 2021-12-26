import pymongo
import json
import time


class Info_Score():

    def __init__(self, paper_folder='paper_rank_result',
                 db='info', collection='paper_info'):
        self.result_file = 'result.json'
        self.db = db
        self.collection = collection
        self.cilent, self.db, self.col = self.connect_db()
        self.result = self.get_result()

    def get_result(self):
        print("开始读取result.josn")
        with open('result.json', 'r') as f:
            datas = json.load(f)
            print("读取result.josn结束")
            return datas

    def connect_db(self):
        cilent = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cilent[self.db]
        col = db[self.collection]

        return cilent, db, col

    def main(self):
        start = time.time()
        print(f'总数为{self.col.estimated_document_count()}')
        mongo_sids = self.col.find({}, {'_id': 1})
        for index, mongo_sid in enumerate(mongo_sids):
            sid = mongo_sid['_id']
            score = self.result.pop(sid, None)
            if score:
                self.col.update_one({'_id': sid}, {"$set": {"score": score}})
            if index % 100000 == 0:
                print(f'>>> {index}\t time:{time.time()-start}')
                start = time.time()


if __name__ == '__main__':
    a = time.time()
    info_score = Info_Score()
    info_score.main()
    print(time.time()-a)
