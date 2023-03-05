# -*-coding:  utf-8 -*-
# @Time    :  2021/3/10 20:24
# @Author  :  Cooper
# @FileName:  爬取百度文库2.py
# @Software:  PyCharm
from selenium import webdriver
import time,re
options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://wenku.baidu.com/view/9816e4ed5122aaea998fcc22bcd126fff7055d86.html")
time.sleep(2)
suspondWindow = driver.find_element_by_xpath('//*[@id="app"]/div/div[14]/div/div')#去除弹窗
suspondWindow.click()
js="var q=document.documentElement.scrollTop=300"#滚动屏幕
driver.execute_script(js)
driver.find_element_by_class_name('foldpagewg-text').click()#点击继续阅读
suspondWindow = driver.find_element_by_xpath('//*[@id="wui-messagebox-cancel-1"]')#第二次去除弹窗
suspondWindow.click()
pattern = re.compile(r'>来自</span><style t(.*?)试读已结束， 剩余0页未读', re.S)
result = pattern.findall(driver.page_source)
pattern = re.compile(r'[\u4e00-\u9fa5]+', re.S)
result = pattern.findall(result[0])
with open('baidu2.txt','w') as f:
    for index,item in enumerate(result):
        if index%11==0:f.write('\n')
        f.write('  '+item)
driver.quit()
