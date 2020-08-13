import time
import json
import os
import csv
import sys
sys.path.append('../')

from Crawler import military_crawl as mc


def main():
    """
    type = [website, category]
    website_list = ['sina', 'sohu']
    category_list = ['china', 'international', 'weapon', 'national_defence', 'univerasl']
    """

    # 抓取新浪网中国军情
    path = 'sina_china_update.csv'
    sina_china = mc.sina_crawler(path, ['sina', 'china'])
    sina_china.get_update_link_list()
    sina_china.get_text()

    # 转为模型可用格式
    with open(path, 'r') as f:
        f_w = open('./data/military_test.json', 'w', encoding='utf-8')
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            line = line[4]
            line = line.replace(' ', '').replace('\n', '').replace('\t', '')
            for sent in line.split('。'):
                sent = sent.strip().replace(' ', '') + '。'
                dic = {}
                dic['text'] = sent
                dic['spo_list'] = ''
                json.dump(dic, f_w, ensure_ascii=False)
                f_w.write('\n')
        f_w.close()

    # 执行预测
    os.system('sh ./script/predict.sh')

    # 处理模型输出，并写入数据库
    dic_list = []
    with open('./data/predict_dev.json', 'r') as f, open('../demo/data/test.json', 'a') as f_w:
        for line in f.readlines():
            dic = json.loads(line)
            if dic['spo_list'] == '':
                continue
            for spo in dic['spo_list']:
                # 查重模块
                # 暂略...
                if spo not in dic_list:
                    dic_list.append(spo)
                    json.dump(spo, f_w, ensure_ascii=False)
                    f_w.write('\n')


if __name__ == "__main__":
    main()
