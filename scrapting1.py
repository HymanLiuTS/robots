#coding:utf-8
import urllib2,re,itertools,time
from bs4 import BeautifulSoup

"""
下载url信息
"""
def download(url,user_agent='MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',proxy=None, num_retyies=2):
    print 'Downloading:',url
    headers={'User_agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    opener=urllib2.build_opener()
    if proxy:
        proxy_param={urlparse.urlparse(url).cheme:proxy}
        opener.add_handler(urllib.ProxyHandler(proxy_param))
    try:
        html=urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retyies>0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retyies)
    return html

"""
按照网站地图获取链接信息
"""
def crawl_sitemap(url):
    try:
        sitemap=download(url)
        print sitemap
        links=re.findall('<loc>(.*?)</loc>',sitemap)
        print links
        for link in links:
            print 'Downloading ',link
            html=download(link)
            print html
    except Exception, e:
        print e.message

"""
按照ID来获取链接信息
"""
def crawl_ID(url,max_errors=5):
    num_errors=0;
    try:
        for page in itertools.count(1):
            url='http://www.codenest.cn/post/%d'%page
            html=download(url)
            if html is None:
                num_errors+=1
                if num_errors==max_errors:
                    break
            else:
                num_errors=0;
                print html
    except Exception as e:
        print "Error",e.message


import urlparse,robotparser

"""
用来统计csnd论坛使用者信息
"""
def csdn_user_count(baseurl,childurl,max_depth=2):
    seen={}
    rp=robotparser.RobotFileParser()
    rp.set_url('http://bbs.csdn.net/robots.txt')
    rp.read()
    user_agent = 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
    try:
        for page in itertools.count(1):
            time.sleep(1)
            #构建根url
            new_url=urlparse.urljoin(baseurl,childurl)+'?page=%d'%page
            depth=seen[new_url]
            if depth==max_depth:
                return
            #获取根url下载页面中所有的连接，如果获取不到说明已经到了尾页，直接退出
            links=get_Links(new_url);
            if(links is None):
                break;
            else:
                #遍历所有的连接获取用户信息
                for link in links:
                    if link not in seen:
                        can=rp.can_fetch(user_agent,link)
                        if can==True:
                            print "Get User info :",link
                            throttle=Throttle(5)
                            throttle.wait(link)
                            get_userinfo(link)
                            seen[link]=depth+1
    except Exception as e:
        print 'csdn_user_count error:',e.message

"""
获取论坛每一页的发帖者链接
"""
def get_Links(url):
    links=[]
    user_info=re.compile('<a href="(.*?)" rel="nofollow"',re.IGNORECASE)
    try:
        html=download(url)
        if html is None:
            return None
        else:
            links=user_info.findall(html)
    except Exception as e:
        print 'get_Links error:',e.message
    return links

"""
获取使用者信息
"""
def get_userinfo(url):
    try:
        html=download(url)
        if html is not None:
            soup=BeautifulSoup(html,'html.parser')
            fixed_html=soup.prettify()
            dt=soup.find('dt',attrs={'class':'person-nick-name'})
            print dt
    except Exception as e:
        print 'get_userinfo error:',e.message

import datetime
class Throttle:
    def __init__(self,delay):
        self.delay=delay
        self.domains={}

    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        print '记录网站访问信息:',domain
        last_accessed=self.domains.get(domain)
        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        self.domains[domain]=datetime.datetime.now()