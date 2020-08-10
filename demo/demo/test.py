import csv
import json


def get_data(filepath):
    datas = []
    with open(filepath) as f:
        csv_book = csv.reader(f)
        for row in  list(csv_book)[1:-1]:
            if row[1] != '':
                datas.append(row)
    return datas


def write_json(filepath, data):
    with open(filepath,'a') as f:
        f.write('[')
        for i in range(len(data)):
            tmp_str = '{\n"spo_list": {\n\t"subject_type": "' + data[i][2] + '",\n\t"subject": "' + data[i][1] \
            + '",\n\t"predicate": "' + data[i][5] + '",\n\t"object_type": "'+data[i][4] + '",\n\t"object": "' \
            + data[i][3].replace('"',"'") + '"\n}\n},\n'
            if i == len(data)-1:
                tmp_str=tmp_str[:-2]
            f.write(tmp_str)
        f.write(']')

filepath = 'D:\\ICE实验室\\sample(搜狐军事兵器解析).csv' # csv地址
jsonfile = 'D:\\ICE实验室\\tmpjson.json'  # 生成的json地址
# datas = get_data(filepath)
# write_json(jsonfile, datas)

with open(jsonfile,'r') as f:
    data=json.load(f)  # 加载为json保存
    entity_tmp_array = []
    entity_array=[]
    data_dict={}
    for row in data:
        tmp_dict={}
        entity_tmp_array.append(row['spo_list']['subject']) # 添加实体名
        tmp_dict['predicate'] = row['spo_list']['predicate']
        tmp_dict['object'] = row['spo_list']['object']
        data_dict[row['spo_list']['subject']]=tmp_dict
    entity_tmp_array=list(set(entity_tmp_array))
print(data)

