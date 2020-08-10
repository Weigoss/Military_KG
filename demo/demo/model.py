import json
from demo.settings import BASE_DIR


def get_tips():
    jsonfile = BASE_DIR + '/data/junshi_data.json'  # 生成的json地址
    with open(jsonfile,encoding='utf-8') as f:
        data=[]
        tmp_row=f.readline()
        while tmp_row:
            data.append(json.loads(tmp_row))
            tmp_row=f.readline()
        entity_array = []
        for row in data:
            entity_array.append(row['spo_list']['subject']) # 添加实体名
        entity_array = list(set(entity_array))
    return entity_array


def get_contact(data,key):
    kf_data=[]
    for row in data:
        row_data = row['spo_list']
        if row_data['subject'] == key:
            tmp_dict = {'source': row_data['subject'], 'target': row_data['object'], 'rela': row_data['predicate'],
                        'type': 'resolved'}
            kf_data.append(tmp_dict)
            if row_data['object']!=key:
                tmp_kf_data=get_contact(data,row_data['object'])
                kf_data.extend(tmp_kf_data)
    return kf_data


def get_data(key):
    jsonfile = BASE_DIR + '/data/junshi_data.json'  # 生成的json地址
    with open(jsonfile,encoding='utf-8') as f:
        data = []  # 读取文件保存数据
        tmp_row = f.readline()
        while tmp_row:
            data.append(json.loads(tmp_row))
            tmp_row = f.readline()
        kf_data = []
        kf_data.extend(get_contact(data,key))
        return kf_data
