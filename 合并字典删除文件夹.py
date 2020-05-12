# -*- coding: utf-8 -*-
"""
Created on Sat May  9 08:39:06 2020

@author: ethan
"""
import json
import os
import shutil
#%%
"""
合并字典
"""
with open("links.json", 'r') as f:
    links1 = json.loads(f.read())
    
with open("links20000.json", 'r') as f:
    links2 = json.loads(f.read())
    
link = {}
link.update(links1)
link.update(links2)

# filename = 'links.json'
# with open(filename, 'w') as f:
#     json.dump(link, fp=f, indent=4)


#%%
"""
删除空文件夹
"""
for (root, dirs, files) in os.walk('data'):
    for item in dirs:
        dir = os.path.join(root, item)
        # print(dir)
        
        try:
            
            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
            # print(dir)
        except Exception as e:
            pass
            # print('Exception',e)

#%%
"""
删除数量太少的文件夹
"""
for (root, dirs, files) in os.walk('data'):
    for item in dirs:
        dir = os.path.join(root, item)
        
        if len(os.listdir(dir)) < 10:
            shutil.rmtree(dir)
            print(dir)