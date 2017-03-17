#coding:utf-8
import sys,re
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2
def download(url,user_agent='hyman',num_retries=3):
    print 'Downloading: ',url
    headers={'User-agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code< 600:
                return download(url,user_agent,num_retries-1)
    return html

def crawl_sitemap(url):
    sitmap=download(url)
    links=re.findall('<loc>(.*?)</loc>',sitmap)
    for link in links:
        html=download(link)
        print html


if __name__=='__main__':
    print download('http://www.codenest.cn')
