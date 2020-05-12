# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:00:04 2020

@author: ethan
"""

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os 
from concurrent.futures import ThreadPoolExecutor
import time

headers = {
    'Cookie': 
    'User-Agent': 
}

def get_infor(url):
    """
    获取该做法的所有步骤，材料，图片链接

    Parameters
    ----------
    url : string
        做法网址.

    Returns
    -------
    dicts： dictionary
        返回一个字典，用于保存json格式.

    """
    try:
        html =requests.get(url, headers=headers,timeout=10)
        html.encoding ='utf-8'
        soup =BeautifulSoup(html.text,'lxml')
    except:
        pass
        # print(str(url) + ' url error')
        
    data = str(soup.find_all('script')[-1])
    dicts = data.split('>')[1].split('<')[0]

    return eval(dicts)


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
    #     for chunk in r.iter_content(chunk_size=512):
    #         f.write(chunk)
    r = requests.get(IMAGE_URL,headers = headers,timeout=30)
    with open(save_path, 'wb') as f:
        f.write(r.content) 
        
def markdir(i):
    """
    为该类菜设置文件夹保存该类菜所有做法。
    因为爬取数据不一定100%成功，所有部分菜名没有获取到，只能保存链接

    Parameters
    ----------
    i : string
        菜名.

    Returns
    -------
    None.

    """
    if i[:5] == 'https':
        save_dir = 'data/' + str(i.split('/')[-1])
        save_image_dir = 'image/'+ str(i.split('/')[-1])
        save_image_dir_512 = 'image_512/' + str(i.split('/')[-1])
        
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)    
        if not os.path.isdir(save_image_dir):
            os.makedirs(save_image_dir)            
        if not os.path.isdir(save_image_dir_512):
            os.makedirs(save_image_dir_512)                
    else:
        save_dir = 'data/' + str(i)
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            
        save_image_dir = 'image/' + str(i)
        if not os.path.isdir(save_image_dir):
            os.makedirs(save_image_dir)
            
        save_image_dir_512 = 'image_512/' + str(i)
        if not os.path.isdir(save_image_dir_512):
            os.makedirs(save_image_dir_512)
        

def save_images(links,i,index,j,url):
    """
    保存照片和做法

    Parameters
    ----------
    links : dictionary
        所有类别菜的链接.
    i : string
        菜名.
    index : int
        第几个菜.
    j : int
        第几个做法.
    url : string
        做法链接.

    Returns
    -------
    None.

    """
    j += 1
    try:
        start = time.time()
        data_dict = get_infor(url)
        end = time.time()
        # print(end - start)
        # print(str(index) +' ' + str(j) + ' ' + str(i) + ' infor get')
    except:
        pass
    if data_dict:        
        filename = 'data/' + str(i) +'/'+ data_dict['keywords'][0] + '_' + str(j) +'.json'
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump(data_dict, fp=f, indent=4)
            image_url = data_dict['image']
            
            #保存512 尺寸
            image_url = image_url.replace(str(200), str(512))
            image_url = image_url.replace(str(300), str(512))
            
            #保存全尺寸
            # if 'png' not in image_url:
            #     image_url = image_url.split('jpg')[0] + 'jpg'
            # else:
            #     image_url = image_url.split('png')[0] + 'png'
                
            save_path = 'image_512/' + str(i) +'/'+ data_dict['keywords'][0]+ '_' + str(j) + '.jpg'
            try:
                chunk_download(image_url,save_path)
                # print(str(index) +' ' + str(j) + ' ' + str(i) + ' save success ' + str(end - start))
            except:
                # print(str(index) +' ' + str(j) + ' ' + filename + ' image save error')
                pass
            
        else:
            print(str(index) +' ' + str(j) + ' ' + filename + ' exists')
            pass
    else:
        pass
    
    # print(str(index) + ' ' + filename + ' save success')
    
def create_dir(index,i,links):
    """
    过滤已经下载好，或者名字出现错误的菜

    Parameters
    ----------
    index : int
        第几个菜.
    i : string
        菜名.
    links : dictionary
        菜的所有链接.

    Returns
    -------
    None.

    """
    if i[:5] == 'https':
        print(str(index) + ' ' + i + ' makedirs funtion error')
        pass
    else:
        save_dir = 'data/' + str(i)
        if os.path.isdir(save_dir):
            print(str(index) + ' ' +  str(i) +' 已有跳过')
            pass
        else:
            markdir(i)
            starts = time.time()
            with ThreadPoolExecutor(max_workers=20) as t:
                for j,url in enumerate(links[i]):
                    t.submit(save_images, links,i,index,j,url)
                print(str(index) + ' ' + str(i) + ' save success')
            ends = time.time()
            print(str(i) + ' Total time cost:' + str(ends - starts))

    
def start_thread(count):
    """
    启动线程池执行下载任务
    最好count数量为1，用时长，但基本爬全
    :return:
    """
    with open("links.json", 'r') as f:
        links = json.loads(f.read())
    print('total: ' + str(len(links)))
    with ThreadPoolExecutor(max_workers=count) as ts:
        for index, i in enumerate(links):
            index += 1
            ts.submit(create_dir, index,i,links)
        
            


if __name__ == "__main__":
    print("程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    startss = time.time()
    start_thread(count)
    endss = time.time()
    print('程序执行结Total time cost:' + str(endss - startss))
    print("程序执行结束")
        
    
