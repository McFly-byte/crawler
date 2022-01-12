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

#每次异常中断就通过80图书馆重新获取SID, 防止掉线
def getSID():
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get(url = "http://www.80lib.com/user/enlist/wose.html")
    # 添加cookie跳过登录 Cookie要去网站手动获取
    Cookie = "PHPSESSID=vot9oap6nll53q0p09934j21jm; _ga=GA1.2.187670977.1637156224; Hm_lvt_550672a265db97bedecf48ee742a872a=1639486131; _gid=GA1.2.252902446.1641866036; loginuser=eyJpdiI6Imd6ZVBmeUpuVmNFYmxnWW1Db1pZS0E9PSIsInZhbHVlIjoiQ1RsVHMwV01pY05IMlwvcFhiVGdZYzB4N2ZZelFVQjNxT1RuUFF1c0ZXa1U9IiwibWFjIjoiZmQ1NGIzZjZkNzMyNDBmZDk4ZGIyMTZjZGVkZWM2NGUyYmVjMzU2ZTZlZjE0MGM0MjBkNTIxY2ZiYzIyMDNlMyJ9; loginpass=eyJpdiI6ImF2OFwvVnJSeE5maFF1WHF1VWVVejJRPT0iLCJ2YWx1ZSI6IkdkampHQndwM2dNOHZxVDlFMW1jUGc9PSIsIm1hYyI6ImEwMTRkY2NjMGYyOWQyZjQ3Yjc3ZWQ4NzE5NTM3NGRhMmU1MGYxYjMwMmJjY2E2NWJjMzZiNGE0MWEwYjY2ZTYifQ%3D%3D; sid=eyJpdiI6ImRtM0Y1RkhuU21oU0VUSDRNUWtGUnc9PSIsInZhbHVlIjoiZVF6VEdTQWdoaUJSa1RkSFlQdTNKSHdoT044endxNVp3bFJYVWxnaHVpNURcLzVBc3pmMFF0NVBKY1Z2aDZ3Vk8iLCJtYWMiOiIwNjZlMjNlMWZjMzUyNmZjNjZhZjZjZWRhZDRmMDUyYjhlNjNhNTU0MDY0YjQwZjY3YWRlMjcyYTY1NDZmODAyIn0%3D; libsid=Fbxo56dzTN2AtSQWKmRQRC2rifd4wa0uyC3i8Pww; libid=6990; ms=wose; XSRF-TOKEN=eyJpdiI6IkhKN0pRTzRDZXJnXC9kVXNiWjlIbkxRPT0iLCJ2YWx1ZSI6IkRSVUJiZVNOaTRxOTc2b05VQmNXK3hrVlRyOEhpTXdDUUJmd1l6a2dwMFV2TlUwYUJEUFo1ckNncEl3bCs4VEIiLCJtYWMiOiJlNWY5MTE3ZGYzYzVlYTAyZmNjZGNlOTRiOTMyNjRhYWNmYmFkMDk1OTNmY2MyZmU3MjBlOWI3NjNhMDI5NjJhIn0%3D; 80lib123_session=eyJpdiI6IjBtdERKeFYrTnRrWnNCSm4wWFl1N2c9PSIsInZhbHVlIjoidmlWbFErYytKdktpdGVkdGs0ZWVTVW1MT3J3RmpsamdcLzA0RjFmcmpYN2plMUF1STE4ZUN3NVU5VEpFSkJGZ3IiLCJtYWMiOiJjY2EyMWMzZDhkMzJmN2E2MTdlM2Y3OTkxY2I4MzJlZjdjM2ZmMDUzYTMzNmE3M2MyMTljZmYxNDZmZjllYTkyIn0%3D; Hm_lpvt_550672a265db97bedecf48ee742a872a=1641911978; _gat_gtag_UA_115631786_1=1"
    Cookie = Cookie.split('; ')
    for attribute in Cookie:
        tmp = attribute.split('=')
        browser.add_cookie({'name':tmp[0],'value':tmp[1]})
    time.sleep(1)
    try:
        divs = browser.find_elements(By.CLASS_NAME,"col-lg-3")
        for div in divs:
            a = div.find_element(By.TAG_NAME,"a")
            b = div.find_element(By.TAG_NAME,"b").text
            if "德温特" in b:
                a_href = a.get_attribute("href")
                print( a_href)
                browser.get(a_href)
                try:
                    browser.find_element(By.XPATH,"//*[@id='p1']/p[3]/a").click()
                    time.sleep(5)
                    cul_url = browser.current_url
                    print("当前网页链接: " + cul_url )
                    SID = (cul_url.split('&')[2]).split('=')[1]
                    print("当前网页SID: " + SID)
                    return SID
                except:
                    continue
    except Exception as e:
        print(e)

# 需要实现：从excel文件中得到专利号，根据专利号访问网站,存储数据，若掉线重新获得SID并继续进行动作
def get_patent_details( num_begin, num_end, index, SID, datalist=[] ):
    length = len(datalist)  # 要操作的专利数目
    # 将输出写入文本文件中
    mylog = open(log_path, mode='a', encoding='utf-8')
    slip = open('slip.txt',mode='a', encoding='utf-8')
    print("=====start=====", file=mylog)

    url = "http://apps.webofknowledge.com/DIIDW_GeneralSearch_input.do?product=DIIDW&SID=" + SID + "&search_mode=GeneralSearch"
    # 进入网站爬取信息
    # 初始化搜索页面
    desired_capabilities = DesiredCapabilities.EDGE
    desired_capabilities["pageLoadStrategy"] = "none"
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    # 遍历区间内每个专利
    for i in range(num_begin, num_end):
        flag = 1  # 施引专利计数
        # 建立一个excel表，以此专利的专利号命名
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        print( datalist[i] + " is being processed.")
        filename = dest_path + "/" + str(index) + "/" + datalist[i] + ".xls"  # 存储路径
        if (os.path.exists(filename)):
            continue
        booksheet.write(0, 0, "专利号")
        #  修改检索方式为专利号
        driver.get(url)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH,"//*[@id='searchrow1']/td[2]/span/span[1]/span/span[2]").click()
        try:
            driver.find_element(By.CLASS_NAME,"select2-search__field").send_keys('专利号')
        except:
            driver.find_element(By.CLASS_NAME,"select2-search__field").send_keys('Patent Number')
        driver.find_element(By.CLASS_NAME,"select2-search__field").send_keys(Keys.ENTER)
        try:
            # 先将搜索框里的内容清空
            ib = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, input_box)))
            ib.send_keys(Keys.CONTROL + 'a')
            ib.send_keys(Keys.DELETE)
            # 输入专利号并检索
            ib.send_keys(datalist[i])
            cb = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,check_btn)))
            cb.click()
            # 得到该专利页面链接，并进入
            pl = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,patent_link)))
            pl.click()
            try:
                # 根据文字内容定位
                if( 'en_US' in driver.current_url ):
                    td = driver.find_element(By.XPATH, patent_cited_by_exmnr[1])
                    a = td.find_element(By.TAG_NAME, 'a')
                    a.click()
                else:
                    td = driver.find_element(By.XPATH, patent_cited_by_exmnr[0])
                    a = td.find_element(By.TAG_NAME, 'a')
                    a.click()
            except Exception as e:
                print(e)
            # 将引用的专利信息导出
            dat = []
            lst = []
            page_amounts = int(driver.find_element(By.ID,'pageCount.top').text)  # 页码数
            print(str(index) + "---" + datalist[i] + "{} 页待爬取".format(page_amounts))
            # 将每一页内容爬取下来
            for pa in range(1, page_amounts + 1):
                print(str(index) + "---" + datalist[i] + " 第{}页 / 共{}页 ".format(pa,page_amounts))
                if (pa == 1):  # 第一页不必输入页数
                    pass
                else:
                    # 页码切换
                    swith_btn = driver.find_element(By.XPATH,switch_xpath)
                    swith_btn.clear()
                    swith_btn.send_keys(str(pa))
                    swith_btn.send_keys(Keys.ENTER)
                    try:  # 检测页面是否加载成功
                        tmp = driver.find_element(By.CLASS_NAME,flag_class).text
                    except: # 不成功刷新页面
                        driver.refresh()
                #TODO 弄清楚下面这段是干嘛的
                th_contents = driver.find_element(By.XPATH,table_xpath).text
                id = th_contents.split('\n')
                id_leng = len(id)
                pu = 2
                while (pu < id_leng - 4):
                    word = id[pu].split(":")[0]
                    if word == '':
                        pu -= 1
                    lst.append(id[pu].split(":")[0])
                    pu += 3
            # 将数据写入excel表中
            for l in range(0, len(lst)):
                booksheet.write(l + 1, 0, lst[l])
            # 将xls文件保存到指定路径
            workbook.save(filename)
            print("The file located in " + filename + " has been saved.")
            print("进程-" + str(index) + "-总进度: " + str(i + 1) + " /   " + str(length), file=mylog)
        except:
            print(time.ctime() + "  PROGRESS-" + str(index) + "-OVERALL: " + str(i + 1) + " /   " + str(length), file=mylog)
            print( datalist[i], file=slip )
            Access_interval[index][0] = i+1
            print(time.ctime() + "  PROGRESS-" + str(index) + "-OVERALL: " + str(i + 1) + " /   " + str(length) )
            continue;
    mylog.close()

# 从本地文件中获得待爬专利专利号
def get_patent_NO( path ):
    datalist = []
    filenames = os.listdir(path)
    for i, filename in enumerate(filenames):
        print('==================第%s个文件=========================' % (i + 1))
        print('文件名：%s' % (filename))
        xlspath = path +"/" +filename
        print( xlspath )
        xls = xlrd.open_workbook(xlspath) #打开excel文件
        sheet = xls.sheets()[0]  #获取第一张表格
        nrows = sheet.nrows  # 获取总行数
        for i in range(1, nrows):
            try:
                a = sheet.cell(i,0).value  # 根据行数来取对应列的值，并添加到字典中
                a = a.split(";")[0] # 根据专利号检索，一次只能检索一条专利号，故取每个专利的首个专利号
                datalist.append(a) # 在列表尾部添加元素
            except:
                print("运行失败{}".format(i))
    return datalist

#TODO 定期删除历史记录以免达到上限无法继续
def history():
    pass

#TODO 变量 收纳 最后再考虑
backlog_path = "Final"
log_path = "log.txt"
dest_path = "achievements"
input_box = "//*[@id='value(input1)']"  # 专利号输入框
check_btn = "[class='large-button primary-button margin-left-10']"  # 检索按钮
patent_link = "[class='smallV110 snowplow-full-record']"  # 专利详细信息链接
amount_xpath = ["//*[@id='FullRecDataTable']/tbody/tr[7]/td/table/tbody/tr/td[1]/a","//*[@id='FullRecDataTable']/tbody/tr[7]/td/table/tbody/tr/td[2]/a"]  # 引用专利数量链接
table_xpath = "//*[@id='records_chunks']/table"  # 专利信息所在的表格
switch_xpath = "//*[@id='summary_navigation']/nav/table/tbody/tr/td[2]/input"  # 换页输入框
flag_class = "NEWpageTitle" # 判断是否加载成功的class
patent_cited_by_exmnr = ["//*[@id='FullRecDataTable']/tbody/tr[7]/td/table/tbody/tr/td[contains(text(),'引用的专利')]",
                         "//*[@id='FullRecDataTable']/tbody/tr[7]/td/table/tbody/tr/td[contains(text(),'cited')]"]
Access_interval = [
    (0, 0),
    (55, 99),
    (164,199),
    (256,299),
    (339,399),
    (456,499)
]
if __name__ == '__main__':
    print(time.ctime())
    # 获取待爬专利号
    datalist = get_patent_NO(backlog_path)

    # TODO 修改循环条件
    while( 1 ):
        SID = getSID()

        one = multiprocessing.Process(target=get_patent_details, args=(Access_interval[1][0], Access_interval[1][1], 1, SID, datalist))
        two = multiprocessing.Process(target=get_patent_details, args=(Access_interval[2][0], Access_interval[2][1], 2, SID, datalist))
        three = multiprocessing.Process(target=get_patent_details, args=(Access_interval[3][0], Access_interval[3][1], 3, SID, datalist))
        four = multiprocessing.Process(target=get_patent_details, args=(Access_interval[4][0], Access_interval[4][1], 4, SID, datalist))
        five = multiprocessing.Process(target=get_patent_details, args=(Access_interval[5][0], Access_interval[5][1], 5, SID, datalist))

        one.start()
        two.start()
        three.start()
        four.start()
        five.start()

        one.join()
        two.join()
        three.join()
        four.join()
        five.join()

#TODO 代码优化提升，提高可重用性
