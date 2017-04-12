#coding:utf-8
import sys,re
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2
def download(url,user_agent='hyman',num_retries=3):
    """
    :param url:想要下载的url
    :param user_agent: 用户代理
    :param num_retries: 服务器内部错误时重复尝试的次数
    :return:url对应的html文本内容
    """
    print 'Downloading: ',url
    #定义用户代理
    headers={'User-agent':user_agent}
    #构造请求对象
    request=urllib2.Request(url,headers=headers)
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            #处理服务器内部错误500，重复进行下载
            if hasattr(e,'code') and 500<=e.code< 600:
                return download(url,user_agent,num_retries-1)
    return html

def crawl_sitemap(url):
    """
    :param url:sitemap网站的url
    :return:
    """
    #下载sitemap
    sitemap=download(url)
    #找到sitemap内所有的loc定位的url
    links=re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        #分别下载每个url中的文档
        html=download(link)
        print html


if __name__=='__main__':
    print crawl_sitemap('http://www.codenest.cn/sitemap.xml')
