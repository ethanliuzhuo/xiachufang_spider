# -*- coding: utf-8 -*-
"""
Created on Fri May  8 08:38:28 2020

@author: ethan
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from concurrent.futures import ThreadPoolExecutor

headers = {
    'Cookie': 
    'User-Agent': 
}
def get_url_and_name(url):
    """
    第一页的信息
    Parameters
    ----------
    url : string
        网站信息.

    Returns
    -------
    link : string
        返回这个菜的链接.
    name : string
        菜名.

    """
    link = []

    # print(url)
    try:
        html =requests.get(url, headers=headers,timeout=10)
        html.encoding ='utf-8'
        soup =BeautifulSoup(html.text,'lxml')
        break_word = str(soup.find_all(name='div',attrs={"class":"wrapper"})[-1]).split('\n')[1] #暂时无用
        name = soup.find('input')['value'] #菜名
        dic = eval(str(soup.find_all('script')[-1]).split('>')[1].split('<')[0])
        for j in dic['itemListElement']:
            link += [j['url']]
        return link,name
    except:
        print(url + ' error')

def get_url_and_names(i,l):
    """
    第二页到第十六页的信息，添加进list里

    Parameters
    ----------
    i : int
        类别.
    l : list
        该类菜的列表.

    Returns
    -------
    l : list
        该类菜的列表.

    """
    for pages in range(2,16):
        # print('pages:',pages)
        url = 'https://www.xiachufang.com/category/1' + str(i).zfill(6) + '/?page=' + str(pages)
        # print(url)
        try:
            html =requests.get(url, headers=headers,timeout=10)
            html.encoding ='utf-8'
            soup =BeautifulSoup(html.text,'lxml')
            break_word = str(soup.find_all(name='div',attrs={"class":"wrapper"})[-1]).split('\n')[1]
            # print([soup.find('input')['value']])
            if break_word == '        下厨房没有这个菜谱......':
                break
            else:
                dic = eval(str(soup.find_all('script')[-1]).split('>')[1].split('<')[0])
                for j in dic['itemListElement']:
                    l += [j['url']]
        except:
            print(str(soup.find('input')['value']) + str(pages) + ' error')
            continue
    return l
#%%
def save_links(i,all_links):
    """
    保存该类菜名的所有做法，储存为json格式
    
    Parameters
    ----------
    i : int
        类别.
    all_links : dict
        把所有菜的链接放入该字典中.

    Returns
    -------
    None.

    """
    url = 'https://www.xiachufang.com/category/1' + str(i).zfill(6)
    # print('i:',i) 
    try:
        l,n = get_url_and_name(url)
        print(n)
    except:
        try:
            l,n = get_url_and_name(url)
            print(n)
        except:
            l = []
            n = str(url)
    
    l = get_url_and_names(i,l)
    all_links[n] = l


    filename = 'links20000.json'
    with open(filename, 'w') as f:
        json.dump(all_links, fp=f, indent=4)
        
def start_thread(count):
    """
    启动线程池执行下载任务
    :return:
    """
    all_links = {}
    
    with ThreadPoolExecutor(max_workers=count) as t:
        for i in range(6300,20000): #类别量
            t.submit(save_links, i,all_links)

            
if __name__ == "__main__":
    print("爬取各类菜的做法程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    start_thread(count)
    print("程序执行结束")
