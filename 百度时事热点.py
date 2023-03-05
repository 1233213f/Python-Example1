import requests
from bs4 import BeautifulSoup

response = requests.get("http://top.baidu.com/buzz?b=1")
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, 'lxml')
target = soup.find_all(attrs={"class": "keyword"})
for each in target:
    text = each.find(attrs={"class": "list-title"}).text
    print(text)
