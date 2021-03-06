#!/usr/bin/python  
#-*- coding: utf-8 -*-
#
# Create by Vincent Chan
#
# baidu search results crawler 

import sys
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import re, random, types

from bs4 import BeautifulSoup 

base_url = 'http://www.baidu.com'

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

# results from the search engine
# basically include url, title,content
class SearchResult:
    def __init__(self):
        self.url= '' 
        self.title = '' 
        self.content = '' 

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url 

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def printIt(self, prefix = ''):
        print 'url\t->', self.url
        print 'title\t->', self.title
        print 'content\t->', self.content
        print 

    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url+ '\n')
            file.write('title:' + self.title + '\n')
            file.write('content:' + self.content + '\n\n')

        except IOError, e:
            logging.error('file error:')
        finally:
            file.close()


class BaiduAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime =  random.randint(60, 120)
        time.sleep(sleeptime)

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    # extract serach results list from downloaded html file
    def extractSearchResults(self, html):
        results = list()
        soup = BeautifulSoup(html)
        div = soup.find('div', id  = 'content_left')
        if (type(div) != types.NoneType):
            lis = div.findAll('table', {'class': 'result'})
            if(len(lis) > 0):
                for li in lis:
                    result = SearchResult()
                    h3 = li.find('h3', {'class': 't'})
                    if(type(h3) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = h3.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    #url = self.extractDomain(url)i
                    
                    if(cmp(url, '') == 0):
                        continue
                    #title = link.renderContents()
                    title = link.text.strip()
                    result.setURL(url)
                    result.setTitle(title)

                    span = li.find('div', {'class': 'c-abstract'})
                    if (type(span) != types.NoneType):
                        #content = span.renderContents()
                        content = span.text.strip()
                        result.setContent(content)
                    results.append(result)
                    if len(results) >= 10:
                        break;
        return results

    # search web
    # @param query -> query key words 
    # @param lang -> language of search results  
    # @param num -> number of search results to return 
    def search(self, query, lang='en', num=10):
        query = query.encode('utf-8') #change query code into utf-8 for chinese
        query = urllib2.quote(query)
        search_results = list()
        #wd 代表关键字 pn 代表页码   cl=3 代表网页搜索
        url = '%s/s?wd=%s&pn={0}' % (base_url, query)
        #str = ''
        retry = 3
        while(retry > 0):
            try:
                request = urllib2.Request(url)
                length = len(user_agents)
                index = random.randint(0, length-1)
                user_agent = user_agents[index] 
                request.add_header('User-agent', user_agent)
                request.add_header('connection','keep-alive')
                response = urllib2.urlopen(request)
                html = response.read() 
                results = self.extractSearchResults(html)
                return results
            except urllib2.URLError,e:
                logging.error('url error:')
                self.randomSleep()
                retry = retry - 1
                continue
            
            except Exception, e:
                logging.error('error:')
                retry = retry - 1
                self.randomSleep()
                continue
        return search_results
        
def test():
    if(len(sys.argv) < 2):
        print 'please enter search query.'
        return
    query = sys.argv[1]
    api = BaiduAPI()
    result = api.search(query)
    for r in result:
        r.printIt()

if __name__ == '__main__':
    test()
