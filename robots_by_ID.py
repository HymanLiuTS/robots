#coding:utf-8
import sys,re,itertools
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

max_errors = 5
num_errors = 0
def id_sitemap():
    for page in itertools.count(1):
        url='http://www.codenest.cn/post/%d'%page
        html=download(url)
        if html == None:
            num_errors+=1
            if num_errors>max_errors:
                break;
        else:
            num_errors=0
            fp=open(str(page)+'.txt','w+')
            fp.write(html)




if __name__=='__main__':
    id_sitemap()
