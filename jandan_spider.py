import os
import requests
from urllib import parse
from bs4 import BeautifulSoup
import base64
from threading import Thread
from time import sleep

index = 0
#headers = {'referer': 'http://jandan.net/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
headers = {'referer': 'http://jandan.net/', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


OUTPUT_DIR = 'jiandan'

# 保存图片
def save_jpg(res_url):
    global index
    html = BeautifulSoup(requests.get(res_url, headers=headers).text, 'html.parser')
    for link in html.find_all('span', {'class': 'img-hash'}):
        imgurl = "http:" + str(base64.b64decode(link.text),'utf-8')
        file_name = os.path.basename(parse.urlparse(imgurl).path)
        file_name = os.path.join(OUTPUT_DIR, file_name)
        try:
            r = requests.get(imgurl, headers=headers)
            r.raise_for_status()  # 请求出错，则直接抛出错误
            with open(file_name, 'wb') as fp:
                fp.write(r.content)
            print("正在抓取第%s张图" % index)
            index += 1
        except:
            pass
        # 等待间隔，避免网络请求太频繁
        sleep(0.5)

def getTotalPage(url):
    totalPage = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser').find('span',{'class': 'current-comment-page'}).text
    return int(totalPage[1:len(totalPage)-1])

def getNextPageUrl(url):
    htmlEle = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser').find('a', {'class': 'previous-comment-page'});
    if htmlEle == None:
        return
    nextPageUrl = "http:" + htmlEle.get('href')
    return nextPageUrl


#  抓取煎蛋妹子图片
if __name__ == '__main__':
    url = 'http://jandan.net/ooxx'
    totalpage = getTotalPage(url)
    for i in range(0, totalpage):
        spider_thread = Thread(target=save_jpg(url), daemon=True)
        spider_thread.start()
        url = getNextPageUrl(url)
        if(url == None):
            continue
        # 等待间隔，避免网络请求太频繁
        sleep(0.5)


