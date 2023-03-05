# -*- coding: utf-8
import urllib2
import urllib
import re,os
import time
import pdfkit
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Liao:
    def __init__(self,init_url,out_put_path):
        self.init_url = init_url
        self.out_put_path = out_put_path
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.file_name = 'liao.pdf'
        self.html_template = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="gb2312">
                            </head>
                            <body>
                            {content}
                            </body>
                            </html>


                            """
    #获取网页内容
    def get_content(self,url):
        try:
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8').encode('GBK')
            return content
#            except urllib2.URLError as e:
            except urllib.error.URLError as e:
            if hasattr(e,"reason"):
                print u"连接页面失败,错误原因",e.reason
                return None


    #获取文章目录url列表
    def get_article_url(self):
        content = self.get_content(self.init_url)
        #print content
        pattern = re.compile(r'<li id="\d.*?" style="margin-left:(\d)em;">.*?<a href="(.*?)">(.*?)</a>.*?</li>',re.S)
        # pattern = re.compile(r'<li id="(\d.*?)" style="margin-left:\dem;">',re.S)
        result = re.findall(pattern,content)
        i = 1
        print len(result)
        # for x in result:
        #     print x[0],x[1]
        #     i+=1
        return result


    #获取文章内容，传入文章的url，返回文章内容
    def get_article_detail(self):
        url_list = self.get_article_url()
        pattern = re.compile(r'<div class="x-wiki-content">(.*?)</div>',re.S)
        # patt_title = re.compile(r'<h4>(.*?)</h4>')
        patt_img = re.compile(r'<img src="(/files/attachments/.*?)"',re.S)
        i = 1
        urls = []
        for item in url_list:
            #获取文章的url
            article_url = 'http://www.liaoxuefeng.com' + item[1]
            url_ind = article_url.split('/')[-1]


            #提取文章标题
            article_title = item[2].replace('/','_')
            title_level = item[0]
            #title_tag = '<center><h' + title_level + '>' + article_title + '</h' + title_level + '></center>'
            title_tag = '<center><h1>' + article_title + '</h></center>'
            #生成html文件名
            html_file = url_ind + '.html'


            #根据文章url，抓取文章内容
            content = self.get_content(article_url)
            article_content = str(re.findall(pattern,content)[0])


            #处理图片的url,加上域名
            def func(m):
                if not m.group(1).startswith("http"):
                    rtn = '<img src="http://www.liaoxuefeng.com' + m.group(1) + '"'
                    return rtn
                else:
                    return '<img src="' + m.group(1) + '"'
            article_content = re.compile(patt_img).sub(func, article_content)


            #将标题加到文章内容中
            article_content = title_tag + article_content
            article_content = self.html_template.format(content=article_content)


            #生成url及文件名列表
            urls.append((url_ind,html_file))


            #写文件
            print 'saving file ' + html_file
            with open(html_file, 'wb') as f:
                f.write(article_content)
        return urls


    #将html保存成pdf
    def save_pdf(self,htmls):
        """
        把所有html文件保存到pdf文件
        """
        options = {
                'page-size': 'Letter',
                'encoding': "UTF-8",
                'custom-header': [
                    ('Accept-Encoding', 'gzip')
                ]
            }
        pdfkit.from_file(htmls, self.file_name, options=options)


init_url = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
out_put_path = 'd:/python/test/output'
liao = Liao(init_url,out_put_path)
urls = liao.get_article_detail()
htmls = [x[1] for x in urls]
liao.save_pdf(htmls)-