import urllib2,re
def download(url,user_agent='hyman',num_retyies=2):
    print 'Downloading:',url
    headers={'User_agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    try:
        html=urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retyies>0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retyies)
    return html

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