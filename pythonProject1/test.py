"""
每次运行前根据log.txt中内容修改该Access_interval中的内容
slip.txt中的内容永远不要动，最后一起重新爬
Cookie可能需要改
"""
import threading
import multiprocessing
import xlrd
import xlwt
import os
import openpyxl
import selenium
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# 需要实现：从excel文件中得到专利号，根据专利号访问网站,存储数据，若掉线重新获得SID并继续进行动作
def get_patent_details( index,SID,Begin,End):
    print( str(index) + "线程中：")
    print(Begin[:])
    print(End[:])
    if Begin[index] > End[index]:
        return
    # 遍历区间内每个专利
    for i in range(Begin[index], End[index]):
        pass
    print( SID )
    Begin[index] = Begin[index] + 10



if __name__ == '__main__':
    Begin = multiprocessing.Array("i", [0,500,600,700,339,900])  # 各线程爬取起终点
    End = multiprocessing.Array("i", [0,599,699,799,399,999])
    print(Begin[:])
    print(End[:])
    print(time.ctime())
    # 获取待爬专利号

    SID = "分割线"
    for i in range(5):
        print( "第{}次".format(i))
        one = multiprocessing.Process(target=get_patent_details, args=(1,SID,Begin,End))
        # w = multiprocessing.Process(target=get_patent_details, args=(2,SID))
        # th = multiprocessing.Process(target=get_patent_details, args=(3,SID))

        one.start()
        # w.start()
        # th.start()

        one.join()
        # w.join()
    # th.join()

    # TODO 修改循环条件
#TODO 代码优化提升，提高可重用性
