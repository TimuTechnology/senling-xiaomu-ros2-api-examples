from sentence_transformers import SentenceTransformer
import time
import numpy as np
import json
import importlib
import os
import ast


supported_lan = [
    'en',
    'de',
    'zh-Hans'
]

for lan in supported_lan:
    print('generate embedding for lan:', lan)
    module = importlib.import_module(f'brain.locale_{lan.replace("-", "_")}')
    
    # 提取以 intent 开头的数组
    intent_arrays = []
    for var_name in dir(module):
        if var_name.startswith('intent') and isinstance(getattr(module, var_name), list):
            intent_arrays.extend(getattr(module, var_name))
    print('last array len:', len(intent_arrays))

    knowledge_path = f'/root/asset/data/knowledge_{lan}.json'
    if os.path.exists(knowledge_path):
        with open(knowledge_path, encoding="utf-8") as f:
            data = ast.literal_eval(f.read())
        intent_arrays.extend(data.keys())
    print('last array len:', len(intent_arrays))
    
    if lan == 'en' or lan == 'zh-Hans':
        model = SentenceTransformer(f'/root/model/brain/{lan}')
    else:
        model = SentenceTransformer('/root/model/brain/default')
    data_path = f'/root/asset/data/embedding_{lan}.json'
    
    print('start encode...')
    embeddings = model.encode(intent_arrays).tolist()
    print('finish encode...')
    dict_data = dict(zip(intent_arrays, embeddings))
    print('start write file...')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(dict_data, f, ensure_ascii=False, indent=2)  # 美化格式
    print('finish embedding for:', lan)


