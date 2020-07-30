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
"""

此版本为目前最新版，之前那个废掉，但这个没有加入采集多页的功能

"""
headers = {
    # 'Cookie': 'BIDUPSID=D98C8D248B79FB29732D8D58272E7015; PSTM=1583717215; BAIDUID=D98C8D248B79FB2971049AB30B7E6141:FG=1; CPROID=D98C8D248B79FB2971049AB30B7E6141:FG=1; BDUSS=EFpanhncXJDQ35yWU9EeTkxWXRiS2hYN35FQ001aFFsamFqZGJzNDJlaG9JYXBlRVFBQUFBJCQAAAAAAAAAAAEAAAAK-IENNDE5NTcxNjg2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGiUgl5olIJeT; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ISBID=D98C8D248B79FB2971049AB30B7E6141:FG=1; ISUS=D98C8D248B79FB2971049AB30B7E6141:FG=1',
    'Cookie': 'BIDUPSID=D98C8D248B79FB29732D8D58272E7015; PSTM=1583717215; BAIDUID=D98C8D248B79FB2971049AB30B7E6141:FG=1; BDUSS=2tTZ3BpdTNmY2ZIU0xOanJzTm9SS2JOMXFvZ0stNzZjRDdNdXhhTGVRVmtyflZlSVFBQUFBJCQAAAAAAAAAAAEAAAAK-IENNDE5NTcxNjg2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGQizl5kIs5eN; H_WISE_SIDS=145269_147885_143879_145827_148320_147895_148193_144117_147682_145333_147280_146537_148001_146969_147762_147829_147637_147890_146573_148524_147347_127969_147238_146550_146454_145418_146653_147024_146732_138425_148458_148185_131423_146499_128699_142208_147528_145601_107317_145289_146339_146824_143507_144966_145607_148070_139884_148346_145396_146791_110085; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __yjsv5_shitong=1.0_7_988b1ef3c9586cadd474c46ae1db08d24fb8_300_1594170818229_112.120.248.192_c60188c4; H_PS_PSSID=1454_31325_32140_31254_32045_32230_32257_31640; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=7; session_name=www.baidu.com; session_id=1594190969483',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
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
        # break_word = str(soup.find_all(name='div',attrs={"class":"wrapper"})[-1]).split('\n')[1] #暂时无用
        name = soup.select('body > div.page-outer > div > div > div.pure-u-2-3.main-panel > div.white-bg.block > div > div.pure-u-3-4.search-result-list > h1') #菜名
        name = str(name).split('>')[1].split('<')[0]
        
        selecto = 'body > div.page-outer > div > div > div.pure-u-2-3.main-panel > div.white-bg.block > div > div.pure-u-3-4.search-result-list > div.normal-recipe-list > ul'
        dic_ = soup.select(selecto)
        
        length = len(str(dic_).split('<a class="gray-font" href="'))
        
        for j in range(1,length):
            selector = 'body > div.page-outer > div > div > div.pure-u-2-3.main-panel > div.white-bg.block > div > div.pure-u-3-4.search-result-list > div.normal-recipe-list > ul > li:nth-child(' + str(j) + ') > div > a'
            dic = soup.select(selector)
            
            link += [str(dic).split('href="')[1].split('"')[0]]
        return link,name
    except:
        print(url + ' error')


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
        print(i,n)
    except:
        try:
            l,n = get_url_and_name(url)
            print(i,n)
        except:
            l = []
            n = str(url)
    
    all_links[n] = l


    filename = 'links42000.json'
    
    with open(filename, 'w') as f:
        json.dump(all_links, fp=f, indent=4)
        
def start_thread(count):
    """
    启动线程池执行下载任务
    :return:
    """
    all_links = {}
    
    with ThreadPoolExecutor(max_workers=count) as t:
        for i in range(42000,45000): #类别量
            t.submit(save_links, i,all_links)

            
if __name__ == "__main__":
    print("爬取各类菜的做法程序执行开始")
    print("======================================")
    print("温馨提示： 输入内容必须为大于的0的数字才行！")
    print("======================================")
    count = int(input("请输入您需要启动的线程数： "))
    start_thread(count)
    print("程序执行结束") 