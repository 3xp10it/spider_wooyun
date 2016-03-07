# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#必须加上上面四行，否则各种编码的错误爆出
from bs4 import BeautifulSoup
import re
import urllib2
import urllib
from urlparse import *
def spider(uri):	
	global all_list
	print uri	
	null_proxy_handler=urllib2.ProxyHandler({})
	opener=urllib2.build_opener(null_proxy_handler)
	urllib2.install_opener(opener)
	req=urllib2.Request(uri)
	req.add_header('user-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)')	
	response=urllib2.urlopen(req)
	html=response.read()
	soup=BeautifulSoup(html,"html.parser")
	for i in soup.find_all(rel="nofollow"):
		each=i.get_text()
		url=urlparse(each)
		url=url.scheme+"://"+url.netloc
		all_list.append(url)
	global temp
	global num_of_all_pages
	global static_uri
	temp+=1	
	print "爬完第%d页".decode('utf-8') % temp 
	if temp==1:		
		static_uri=uri[0:-1]
		all_text=soup.get_text().decode('utf-8')
		p='共.*条(.*)页'.decode("utf-8")
		#这里使用u'共\d{3,4}条.*(\d{2,3})页.*'无法匹配到，可能是因为pattern为u'...'时,\d匹配不到数字
		se=re.search(re.compile(p),all_text)
		result1=se.group()
		print result1
		se1=re.search(re.compile(r'\d{3,4}.*(\d{2,3})'),result1)
		num_of_all_pages=int(se1.group(1))
	next_ur=temp+1	
	next_uri=static_uri+"%s" % str(next_ur)
	print 'next_uri is %s' % next_uri

	print 'temp:%d' % temp
	print 'num_of_all_pages:%s' % num_of_all_pages
	if temp<num_of_all_pages:
		spider(next_uri)
all_list=[]
temp=0
num_of_all_pages=0
static_uri=""
spider("http://www.wooyun.org/corps/page/1")
print all_list
f=open("targets.txt","a+")
for each in all_list:
	f.write(each+'\n')
f.close()
