# 去掉slip.txt中的重复数据
import os

# 获取数据
path = "slip.txt"
datalist = []
with open(path,'r+',encoding='utf-8') as f:
    datalist = f.read().splitlines()
    f.truncate(0)   # 清空文件内容
print( datalist)
# 去重复
NewData = []
for item in datalist:
    if item not in NewData:
        NewData.append(item)
print(NewData)
# 写回（覆盖）
with open(path,'r+',encoding='utf-8') as f:
    for item in NewData:
        f.write(item + '\n')