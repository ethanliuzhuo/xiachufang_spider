# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:40:30 2020

@author: ethan
"""

import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os 
from concurrent.futures import ThreadPoolExecutor
import time
    

headers = {
    'Cookie': 'BIDUPSID=D98C8D248B79FB29732D8D58272E7015; PSTM=1583717215; BAIDUID=D98C8D248B79FB2971049AB30B7E6141:FG=1; CPROID=D98C8D248B79FB2971049AB30B7E6141:FG=1; BDUSS=EFpanhncXJDQ35yWU9EeTkxWXRiS2hYN35FQ001aFFsamFqZGJzNDJlaG9JYXBlRVFBQUFBJCQAAAAAAAAAAAEAAAAK-IENNDE5NTcxNjg2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGiUgl5olIJeT; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ISBID=D98C8D248B79FB2971049AB30B7E6141:FG=1; ISUS=D98C8D248B79FB2971049AB30B7E6141:FG=1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
}

def chunk_download(IMAGE_URL,save_path):
    """
    下载图片

    Parameters
    ----------
    IMAGE_URL : string
        图片URL.
    save_path : string
        保存路径.

    Returns
    -------
    None.

    """
    # r = requests.get(IMAGE_URL, stream=True,headers = headers,timeout=60)    
    # with open(save_path, 'wb') as f:
    #     for chunk in r.iter_content(chunk_size=256):
    #         f.write(chunk)
    r = requests.get(IMAGE_URL,headers = headers,timeout=120)
    with open(save_path, 'wb') as f:
        f.write(r.content) 
    
def save_image(image_url,item_name,name,i):
    """
    保存全尺寸图片，png格式或者jpg格式

    Parameters
    ----------
    image_url : string
        该类菜的所有做法链接.
    item_name : string
        菜名.
    name : string
        做法名字.
    i : int
        第几个.

    Returns
    -------
    None.

    """
    if 'png' not in image_url[i]:
        
        IMAGE_URL = image_url[i].split('jpg')[0] + 'jpg'
        
        save_path  = 'image/' + item_name + '/' + name[i] + '.jpg'
        if not os.path.exists(save_path):
            print(str(i) + ' ' + image_url[i].split('jpg')[0] + 'jpg')
            start = time.time()
            try:
                chunk_download(IMAGE_URL,save_path)
            except:
                print('error')
                pass
            end = time.time()
            print('time:' + str(end-start))
        else:
            print(str(i) + ' ' + save_path + ' exists')
            pass
    else:
        
        IMAGE_URL = image_url[i].split('png')[0] + 'png'
        save_path  = 'image/' + item_name + '/' + name[i] +  '.png'
        if not os.path.exists(save_path):
            print(str(i) + ' ' + image_url[i].split('png')[0] + 'png')
            start = time.time()
            try:
                chunk_download(IMAGE_URL,save_path)
            except:
                print('error')
                pass
            end = time.time()
            print('time:' + str(end-start))
        else:
            print(str(i) + ' ' + save_path + ' exists')
            pass
        
#%%
def start_thread(count):
    """
    启动线程池执行下载任务，下载目录下的所有全尺寸图片
    :return:
    """
    # json_path = []
    path = 'data'
    for path_name in os.listdir(path):
        path_data = path + '/' + path_name
        item_name = path_name
        
        json_name = os.listdir(path_data)
        
        image_url = []
        name = []
        for i in json_name:
            jaso_path = path_data + '/' + i
            print(jaso_path)
            with open(jaso_path, 'r') as f:
                data = json.loads(f.read())
                
            image_url += [data['image']]
            name += [data['keywords'][0]]
    # print(image_url)
        if image_url != []:
            
            with ThreadPoolExecutor(max_workers=count) as t:
                for i in range(len(image_url)):
                    t.submit(save_image,image_url,item_name,name,i)
        else:
            print(str(image_url) + '[]')
                
if __name__ == "__main__":
    print("程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    start_thread(count)
    print("程序执行结束")