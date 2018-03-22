import urllib
import urllib.request
import re
import threading
import time
from BloomFilter import BloomFilter

urlList = ["https://www.pexels.com/"]
deepth = 2
L = threading.Lock()

class ThreadCrawler(threading.Thread):
    count = -1
    filter = BloomFilter(1000)
    def __init__(self, seeds, threadId, savepath):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.current_deepth = 1
        self.links = linkStack()
        self.savepath = savepath
        if isinstance(seeds, str):
            L.acquire()
            ThreadCrawler.filter.set(seeds)
            L.release()
            self.links.addLink(seeds)
        if isinstance(seeds, list):
            for i in seeds:
                L.acquire()
                ThreadCrawler.filter.set(i)
                L.release()
                self.links.addLink(i)

    def run(self, crawl_deepth = deepth):
        while not self.links.isEmpty():
            visitedUrl = self.links.removeLink()
            if visitedUrl is None:                                     #遇到None证明一层的结束
                visitedUrl = self.links.removeLink()
                self.current_deepth -= 1                                #将当前遍历的深度减一，以便返回处同一层其他元素往下遍历
            links = ThreadCrawler.getHtmlList(visitedUrl)
            self.getImg(visitedUrl)
            L.acquire()
            ThreadCrawler.filter.set(visitedUrl)
            L.release()
            if self.current_deepth <= crawl_deepth:
                self.links.addLink(None)                               #标记一层的开始
                for link in links:
                    if not (ThreadCrawler.filter.test(link)):          #如果该网址没有访问过，加入待访问序列
                        self.links.addLink(link)
            self.current_deepth += 1

    def getHtmlList(url):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        referer = "https://www.pexels.com/"
        headers = {"User-Agent": user_agent, "Referer": referer}
        request = urllib.request.Request(url, None, headers)
        try:
            page = urllib.request.urlopen(request, timeout=5)
            html = page.read()
        except:
            return None
        html = html.decode('utf-8')
        reg = r'.*href="(/photo/.*)".*'
        htmlreg = re.compile(reg)
        htmlList = re.findall(htmlreg, html)
        for i in range(len(htmlList)):
            htmlList[i] = "https://www.pexels.com/" + htmlList[i]
        return htmlList


    def getImg(self,url):
        import socket
        socket.setdefaulttimeout(120)
        imglist = []
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')]
        urllib.request.install_opener(opener)
        html = self.getHtml(url)
        reg = r'.*src="(https://images.pexels.com/photos/.*?.jpeg\?).*(auto=compress&amp;cs=tinysrgb).*"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        time.sleep(1)
        for imgurl in imglist:
            imgurl = imgurl[0] + imgurl[1]
            L.acquire()
            print(self.threadId, imgurl)
            ThreadCrawler.count += 1
            L.release()
            try:
                urllib.request.urlretrieve(imgurl, self.savepath + '/%s.jpg' % ThreadCrawler.count)
            except:
                continue

        return imglist


    def getHtml(self, url):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        referer = "https://www.pexels.com/"
        headers = {"User-Agent": user_agent, "Referer": referer}
        request = urllib.request.Request(url, None, headers)
        page = urllib.request.urlopen(request)
        html = page.read()
        html = html.decode('utf-8')
        return html


class linkStack:
    def __init__(self):
        self.links = []

    def addLink(self, url):
        self.links.append(url)

    def removeLink(self):
        try:
            result = self.links.pop()
            return result
        except:
            return None

    def isEmpty(self):
        return len(self.links) == 0


def main(static_url, savepath):
    urlList = ThreadCrawler.getHtmlList(static_url)   #初始化urlList，用以创建线程
    threads = []
    for i in range(len(urlList)):
        t = ThreadCrawler(urlList[i], i, savepath)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    for i in urlList:
        main(i, "G:/桌面/数据结构大作业/bloomTest")