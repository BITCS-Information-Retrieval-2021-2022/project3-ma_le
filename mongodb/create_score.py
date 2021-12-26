from pathlib import Path
import json
import time


class Score():

    def __init__(self, paper_folder='paper_rank_result', start=1, end=6000):
        self.paper_folder = Path(paper_folder)
        self.start = start
        self.end = end

    def main(self):
        datas = {}
        for index in range(self.start, self.end):
            with open(self.paper_folder/f'citationLine{index}'/'part-00000',
                      'r') as f:
                lines = f.readlines()
                for line in lines:
                    sid, score = eval(line)
                    score += datas.get(sid, 0)
                    datas[sid] = score

                if index % 100 == 0 or index == 5999:
                    with open(f'result_{index}.json', 'w') as f:
                        json.dump(datas, f)
                        print(f'写入result_{index}.json')
                print(f'>>>{index:04}/5999\t成功处理{len(lines)}条数据，'
                      f'共有{len(datas)}条数据')


if __name__ == '__main__':
    start = eval(input('请输入开始数：'))
    end = eval(input('请输入结束数：'))
    a = time.time()
    score = Score(start=start, end=end)
    score.main()
    print(time.time() - a)
