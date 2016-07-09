import urllib2
from BeautifulSoup import BeautifulSoup
page = BeautifulSoup(urllib2.urlopen("http://www.readcomics.net/the-flash-rebirth/chapter-1/full"))
arr = page.findAll('img')
for i in arr:
	print i