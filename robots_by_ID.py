#coding:utf-8
import sys,re,itertools
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

#最大的错误次数
max_errors = 5
#已经出错的次数
num_errors = 0
def crawl_id():
    #迭代获取文章的id
    for page in itertools.count(1):
        url='http://www.codenest.cn/post/%d'%page
        html=download(url)
        if html == None:
            num_errors+=1
            if num_errors>max_errors:
                break;
        else:
            num_errors=0
            #将下载的网页保存到本地文件中
            fp=open(str(page)+'.txt','w+')
            fp.write(html)




if __name__=='__main__':
    crawl_id()
