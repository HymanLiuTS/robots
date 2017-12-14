#coding:utf-8

users=set()

import urllib2
def download(url,user_agent='MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',proxy=None, num_retyies=2):
    """
    下载url的内容，返回html文本
    :param url: 要下载的url
    :param user_agent: 用户代码
    :param proxy: 服务器代理
    :param num_retyies: 遇到服务端错误时重复下载的次数
    :return: 返回下载的html文本
    """
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

import urlparse,itertools,lxml.html
def get_csdn_user_info(baseurl,field):
    """
    获取csdn论坛上注册人员的信息
    :param baseurl:基本url，比如http://bbs.csdn.net/forums/
    :param field:，分类字段，比如CSharp
    :return:无
    """
    links=[]
    users=set()
    try:
        for page in itertools.count(1):
            url=urlparse.urljoin(baseurl,field)+'?page=%d'%page
            html=download(url)
            if html is None:
                return
            callback=ScrapeCallback()
            links.extend(callback(url,html) or [])
            print "len(links)",len(links)
    except Exception as e:
        print "get_csdn_user_info error:",e.message

import csv
class ScrapeCallback:
    """
    回调类，用于向csv文件中写入信息并返回获取到的新的url
    """
    def __init__(self):
        try:
            self.writer=csv.writer(open('users.csv','a'))
            self.fields=('user','rul')
            self.writer.writerow(self.fields)
        except Exception as e:
            print "__init__ error:",e.message

    def __call__(self, url,html):
        dic={}
        try:
            tree=lxml.html.fromstring(html)
            links = tree.cssselect('td.tc>a[rel=nofollow]')
            for link in links:
                name=link.text_content()
                info_link=link.get('href')
                if name not in users:
                    row=[]
                    row.append(name)
                    row.append(info_link)
                    self.writer.writerow(row)
                    users.add(name)
            return links
        except Exception as e:
            print "__call__ error:",e.message
