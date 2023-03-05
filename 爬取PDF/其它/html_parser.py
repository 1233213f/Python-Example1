import re
import urllib.parse
from bs4 import BeautifulSoup
class HtmlParser(object):
  def parse(self, page_url, html_cont):
    if page_url is None or html_cont is None:
      return
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    new_urls = self._get_new_urls(page_url, soup)
    print("parse new_urls %s" % new_urls)
    new_data = self._get_new_data(page_url, soup)
    return new_urls, new_data
  def _get_new_data(self, page_url, soup):
    res_data = {}
    res_data['url'] = page_url
    print(page_url)
    title_node = soup.find(class_="title").find("h1")
    print(title_node.get_text())
    res_data['title'] = title_node.get_text()
    print("_get_new_data")
    summary_node = soup.find('pre')
    print(summary_node.get_text())
    res_data['summary'] = summary_node.get_text()
    return res_data
  def _get_new_urls(self, page_url, soup):
    new_urls = set()
    links = soup.find_all('a', href=re.compile(r"/jiangnan/"))
    print(links)
    for link in links:
      new_url = link['href']
      new_full_url = urllib.parse.urljoin(page_url, new_url)
      new_urls.add(new_full_url)
      # print(new_full_url)
    return new_urls