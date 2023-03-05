import os
import requests
import re
from bs4 import BeautifulSoup
import time
import logging

# --------------------log记录---------------
# 创建一个logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
# 创建一个handler，用于写入日志文件
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
'''
# 再创建一个handler，用于输出到控制台 
ch = logging.StreamHandler() 
ch.setLevel(logging.DEBUG)'''

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(handler)
# logger.addHandler(ch)
# 下载文件
def DownloadPdf(url):
    #print("1")
    try:
        filename = url.split('/')[-1]   #以/为分割符保留最后一段
        #如果文件不存在
        if (not os.path.exists(filename)):
            r = requests.get(url, headers = header1)
            f = open(filename,"wb")
            f.write(r.content)
            f.close()
            print("download ok")
            logger.info("download ok")  #log记录
        else:
            print("文件已经存在，跳过下载")
            logger.info("文件已经存在，跳过下载")  #log记录
    except Exception as reason:
        logger.info("出错原因：%s" %str(reason))  #log记录
        print("出错原因：%s" %str(reason))


# books网站一共840页面
def getPage(url):
    try:
        page = requests.get(url, headers=header1)  # 获取每一页的html,每一页的html没有pdf文档
        html = page.content
        return html
    except e as reason:
        logger.info("出错原因：%s" % str(reason))  # log记录


# 获取每本书页面的pdf
def getPdfPage(bookurl):
    html2 = getPage(bookurl)
    # print(html)
    soup2 = BeautifulSoup(html2, "lxml", from_encoding='utf-8')  # 网页为lxml格式
    # 查找pdf文件下载的节点
    tags2 = soup2.find_all('span', class_="download-links")
    logger.info("pdf tags：%s" % str(tags2))  # log记录
    # print(tags2)
    # move_list = []

    # re测试
    '''print("re测试")
    for list2 in tags2:
        move = list2.a.span.text.strip()
        move_list.append(move)
    print(move_list)'''

    for list2 in tags2:
        try:
            herf2 = list2.find_all('a')
            # 正则匹配，每本书介绍页面的url
            bookDownloadUr = str(re.findall("http?://(?:[-\w.])+/(?:[-\w.])+/(?:[-\w.,'\s.])+", str(herf2)))
            print(bookDownloadUr)
            logger.info(bookDownloadUr)  # log记录
            # 移除字符串首尾的[]'"
            bookDownloadUrl = bookDownloadUr.strip("[']")
            bookDownloadUrl = bookDownloadUrl.strip('"')
        except Exception as reason:
            logger.info("出错原因：%s" % str(reason))  # log记录

        # 匹配 pdf文档
        if '.pdf' in bookDownloadUrl:
            if '.epub' in bookDownloadUrl:
                print('')
            else:
                print("下载书籍网址：" + bookDownloadUrl)
                logger.info("下载书籍网址：%s" % str(bookDownloadUrl))  # log记录
                DownloadPdf(bookDownloadUrl)
                # return bookDownloadUrl
        else:
            print('epub文件，跳过下载')
            logger.info('epub文件，跳过下载')  # log记录


# 获取每页的10本书的url
def getPageList(html):
    soup = BeautifulSoup(html, "lxml", from_encoding='utf-8')  # 网页为html格式
    # 查找所有有关的节点
    tags = soup.find_all('h2', class_="entry-title")
    # tags = soup.find('h2', class_="entry-title")

    for list1 in tags:
        try:
            herf = list1.find_all('a')
            bookname = herf[0].string  # 每页书籍的名称
            logging.info("书籍名称：%s" % str(bookname))

            # 正则匹配，每本书介绍页面的url
            booku = str(re.findall('http?://(?:[-\w.])+/(?:[-\w.])+', str(herf)))

            # 移除字符串首尾的[]
            bookurl = booku.strip("[']")
            getPdfPage(bookurl)

        except Exception as reason:
            logger.info("出错原因：%s" % str(reason))  # log记录

        # bookurl = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(herf))
        # print(bookurl)
        # print(herf[0].string)  #每页书籍的名称
        # 每次休眠4秒钟，防止对方服务器崩溃。
        time.sleep(4)


# 创建文件夹
def makedir(dirNum):
    # 路径归为
    os.chdir(cp)  # 切换原始路径

    filepathName = str(dirNum)
    isExists = os.path.exists(filepathName)
    if not isExists:
        os.mkdir(filepathName)
        print(filepathName + '文件夹创建成功')
        logger.info(filepathName + '文件夹创建成功')

    file = '\%s' % filepathName  # 刚刚创建的那个文件夹的相对路径
    path = os.path.join(cp + file)  # 刚刚创建的那个文件夹的绝对路径
    os.chdir(path)  # 切换路径


def main():
    print('----爬虫下载程序----')
    url = "http://www.allitebooks.org/page/"
    # 第一页目录
    dirNum = 1
    mkdir(dirNum)
    # os.chdir(os.path.join(cp+ '\%s'%dirNum)) #切换路径

    '''测试记录：5页ok，6-31 linux下载'''
    for pageNum in range(1, 840):  # 从第1页到第2页,有840页。每页10本书

        '''创建文件夹,每5页，即50本书创建一个文件夹'''
        if pageNum % 5 == 0:
            dirNum = dirNum + 1
            makedir(dirNum)
            # 爬虫网址
        print("pageNum = " + str(pageNum))
        logger.info("pageNum = " + str(pageNum))
        urlNew = url + str(pageNum)
        getPageList(getPage(urlNew))
        # testSavePdf()


if __name__ == "__main__":
    main()