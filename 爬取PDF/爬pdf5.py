import requests
import os
import json


def savePng(url, fileName):
    root = "//home//Desktop//"
    path = root + "//" + fileName
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        r.raise_for_status()
    with open(path, "wb+") as f:
        f.write(r.content)


def getPNGName(url):
    req = requests.get(url)
    json_req = req.content.decode()
    json_dict = json.loads(json_req)
    print(json_dict)
    return json_dict["NextPage"]


def getNextPageURL(pngName):
    url = "https://view42.book118.com/pdf/GetNextPage/?f=dXAyMjI2LTIuYm9vazExOC5jb20uODBcMzQ4NDU0MS01OTgxMGI5MDMwM2JjLnBkZg==&img=%s&isMobile=false&isNet=True&readLimit=kVJSwRWfuu2BpuMVDJqlnw==&furl=o4j9ZG7fK94kkYRv4gktA2rYw4NlKHsQghNfCDpGDtCDuhClp@zqsXbBvWkfutt7oIxYGVjQwpqa2_7Y@T__cVzRwC_U6kA_a5K64MvXGRoemz@A5sruig==" % pngName
    return url


def getCurPageUrl(pngName):
    url = "https://view42.book118.com/img/?img=%s" % pngName
    return url


# url = getNextPageURL("7o@o7xcocmmKnrqreQGENvFMksKYwld1WTnrOUUaeADxViDtQ3Pv9cm31oOktykHcA4m4rqRBGs=")
url = "https://view42.book118.com/pdf/GetNextPage/?f=dXAyMjI2LTIuYm9vazExOC5jb20uODBcMzQ4NDU0MS01OTgxMGI5MDMwM2JjLnBkZg==&img=7o@o7xcocmmKnrqreQGENvFMksKYwld1WTnrOUUaeADxViDtQ3Pv9R7mPNB3WAYh&isMobile=false&isNet=True&readLimit=kVJSwRWfuu2BpuMVDJqlnw==&furl=o4j9ZG7fK94kkYRv4gktA2rYw4NlKHsQghNfCDpGDtCDuhClp@zqsXbBvWkfutt7oIxYGVjQwpqa2_7Y@T__cVzRwC_U6kA_a5K64MvXGRoemz@A5sruig=="
for curPageIndex in range(0, 486):
    # 根据当前图片名字，请求下一张图片名字
    pngName = getPNGName(url)
    # 根据下一张图片名字拼凑url
    url = getCurPageUrl(pngName)
    # 下载PNG，记录图片名字
    savePng(url, str(curPageIndex) + ".PNG")
    # 得到下一页图片url
    url = getNextPageURL(pngName)