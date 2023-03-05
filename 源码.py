# _*_ encoding:utf-8 _*_

'''

Created on 2017年8月4日

@author: wangs0622

'''

import urllib2

def download(url):

print "downloading " ,  url

try:

html = urllib2.urlopen(url).read()

except urllib2.URLError as e:

print ("download error: " , e.reason)

html = None

return html

if __name__ == '__main__':

download('http://www.wangs0622.com/dex')