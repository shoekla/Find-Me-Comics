import urllib2
import re
import csv
import time
import requests
import string
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import os


def is_in_arr(lis,s):
	result=False
	for item in lis:
		if item==s:
			result=True
	return result
def deleteDuplicates(lis):
	newLis=[]
	for item in lis:
		if item not in newLis:
			newLis.append(item)
	return newLis
def crawlComicPages(url):
	try:
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		arr = []
		check = 0
		for link in soup.findAll('img'):
			href=link.get('src')
			href_test=str(href)
			if ".png" not in href_test:
				arr.append(href_test)
		return arr
	except Exception,e:
		print str(e)

def crawl(url):
	try:
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		print "E"
		for link in soup.findAll('a'):
			print "For"
			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if "/torrent" in href_test:
				if "http" not in href_test:
					return "https:"+str(href)
	except Exception,e:
		print str(e)

def crawlImg(movie):
	try:
		movie = movie.replace(" ","+")
		url = "http://www.bing.com/images/search?q="+str(movie)+"&FORM=HDRSC2"
		print url
		pages = []
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('img'):

			href=link.get('src')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "1.1" in href:
					return href

	except:
		print "Error at: "+str(url)
def takeoutHTML(lyric) :
	res = ""
	count = 0
	for i in lyric:
		if i == '<':
			count = 1 
		if i == '>':
			count = 2
		if count == 0 :
			if i == '"':
				res = res + "'"
			else :
				res = res + str(i)
		if count == 2 :
			res = res + " "
			count = 0
	res = res.replace("<br/>"," ")
	return res

def getStatus(name):
	name = name.replace(" ","-")
	url = "http://www.readcomics.tv/comic/"+name+""
	source_code=requests.get(url)
	plain_text=source_code.text
	index = plain_text.find("Status")
	index2 = plain_text.find("</tr>",index)
	res = takeoutHTML(plain_text[index:index2])
	res= res.replace("  ","")
	res = res.replace("\n","")
	return res
def getGenre(name):
	name = name.replace(" ","-")
	url = "http://www.readcomics.tv/comic/"+name+""
	source_code=requests.get(url)
	plain_text=source_code.text
	index = plain_text.find("Genre")
	index2 = plain_text.find("</tr>",index)
	res = takeoutHTML(plain_text[index:index2])
	res= res.replace("  ","")
	res = res.replace("\n","")
	return res
def getIssuse(name):
	arr = []
	name = name.replace(" ","-")
	url = "http://www.readcomics.tv/comic/"+name+""
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	arr = []
	check = 0
	for link in soup.findAll('a'):
		chName = link.get('class')
		if chName != None:
			href=link.get('href')
			href_test=str(href)
			if href_test == "None":
				pass
			else:
				if "chapter-00/" not in href_test:
					if "chapter-" in href_test:
						if name in href_test:
							arr.append(str(href_test))
	return deleteDuplicates(arr)
def getIssueName(name):
	index = name.find("chapter-")
	index2 = name.find("-",index)
	return name[index2+1:]
def getPop():
	arr = []
	url = "http://www.readcomics.tv/"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	arr = []
	check = 0
	for link in soup.findAll('a'):
		chName = link.get('class')
		if chName != None:
			href=link.get('href')
			href_test=str(href)
			if href_test == "None":
				pass
			else:
				if "chapter-00/" not in href_test:
					if "chapter-" in href_test:
						arr.append(str(href_test))
	return deleteDuplicates(arr)	

def getPicFromName(name):
	name = name.replace(" ","-")
	url = "http://www.readcomics.tv/comic/"+name
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	for link in soup.findAll('img'):
		href=link.get('src')
		href_test=str(href)
		if "logo" not in href_test:
			return href
def getPic(url):
	index = url.find("/" , url.find(".tv"))
	index2 = url.find("/",index+1)
	return getPicFromName(url[index+1:index2])
def getHomeLink(url):
	index = url.find(".tv/")
	index2 = url.find("/",index+5)
	rea = url[index+4:index2]
	return rea
def searchComic(name):
	arr = []
	name = name.lower()
	namesArr = name.split(' ')
	name = name.replace(" ","+")
	url = "http://www.readcomics.tv/comic-search?key="+name+""
	print "Url: "+url
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	arr = []
	check = 0
	for link in soup.findAll('a'):
		chName = link.get('class')
		if chName != None:
			href=link.get('href')
			href_test=str(href)
			if href_test == "None":
				pass
			else:
				href_test = href_test.replace("comic/","")
				for n in namesArr:
					if n in href_test:
						if href_test.endswith("/"):
							arr.append(str(href_test))
						else:
							arr.append(str(href_test)+"/")
						break
	return deleteDuplicates(arr)	

#print getIssueName("http://www.readcomics.net/harley-quinn/chapter-26")

#print getHomeLink("http://www.readcomics.tv/harley-quinn/chapter-26")

