#encoding:utf-8
from selenium import webdriver
import time
import re
import xlwt
from bs4 import BeautifulSoup
#无模拟界面操作
options=webdriver.ChromeOptions()
options.add_argument('--headless')
driver=webdriver.Chrome(options=options)
url = "https://finance.sina.com.cn/7x24/?tag=2"
driver.get(url)
time.sleep(5)

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(2)
    html = driver.page_source
    if "20201209" in html:
        break


html = driver.page_source
soup = BeautifulSoup(html,'lxml')
message = soup.find_all(name='div',class_="bd_i bd_i_og bd_i_focus clearfix")

dict1 = {}
for i in range(len(message)):
    dict1[i+1]=[message[i].attrs['data-time'],message[i].find('p',class_="bd_i_time_c").string,message[i].find('p',class_='bd_i_txt_c').string]


workbook = xlwt.Workbook('utf-8')
sheet = workbook.add_sheet('sheet1')
sheet.write(0, 0, '日期')
sheet.write(0, 1, '时间')
sheet.write(0, 2, '内容')

for i in range(len(dict1)):
    sheet.write(i + 1, 0, dict1[i+1][0])
    sheet.write(i + 1, 1, dict1[i+1][1])
    sheet.write(i + 1, 2, dict1[i+1][2])

workbook.save('C:/Users/Captain/Desktop/舆论舆情对经济板块影响/数据/新闻/新浪财经新闻爬取行业.xls')
print('已将数据保存至excel！')
