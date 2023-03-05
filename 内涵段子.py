# encoding=utf-8
import urllib.request

import re


class neihanba():
    def spider(self):
        '''
        爬虫的主调度器
        '''
        isflow = True  # 判断是否进行下一页
        page = 1
        while isflow:
            url = "http://www.neihanpa.com/article/list_5_" + str(page) + ".html"
            html = self.load(url)
            self.deal(html, page)
            panduan = raw_input("是否继续(y/n)!")
            if panduan == "y":
                isflow = True
                page += 1
            else:
                isflow = False

    def load(self, url):
        '''
        针对url地址进行全部爬去
        :param url: url地址
        :return: 返回爬去的内容
        '''
        header = {
            "User-Agent": " Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
        }
        request = urllib.request(url, headers=header)
        response = urllib2.urlopen(request)
        html = response.read()
        return html

    def deal(self, html, page):
        '''
        对之前爬去的内容进行正则匹配，匹配出标题和正文内容
        :param html:之前爬去的内容
        :param page: 正在爬去的页码
        '''
        parrten = re.compile('<li class="piclist\d+">(.*?)</li>', re.S)
        titleList = parrten.findall(html)
        for title in titleList:
            parrten1 = re.compile('<a href="/article/\d+.html" rel="external nofollow" >(.*)</a>')
            ti1 = parrten1.findall(title)
            parrten2 = re.compile('<div class="f18 mb20">(.*?)</div>', re.S)
            til2 = parrten2.findall(title)
            for t in ti1:
                tr = t.replace("<b>", "").replace("</b>", "")
                self.writeData(tr, page)
            for t in til2:
                tr = t.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("<br />", "").replace(
                    "&ldquo", "\"").replace("&rdquo", "\"")
                self.writeData(tr, page)

    def writeData(self, context, page):
        '''
        将最终爬去的内容写入文件中
        :param context: 匹配好的内容
        :param page: 当前爬去的页码数
        '''
        fileName = "di" + str(page) + "yehtml.txt"
        with open(fileName, "a") as file:
            file.writelines(context + "\n")


if __name__ == '__main__':
    n = neihanba()
    n.spider()