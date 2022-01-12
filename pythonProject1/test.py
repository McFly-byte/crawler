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

if __name__ == '__main__':
    SID = getSID()
    print( SID )