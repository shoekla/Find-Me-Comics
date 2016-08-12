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

from firebase import firebase

firebase = firebase.FirebaseApplication('https://findmecomics.firebaseio.com/', None)
userName = ""
myComics = []
comicList = []
pop = []
images = []
ips = []
def addIp(ip):
	global ips
	ips.append(str(ip))
def logout(ip):
 	global userName
 	global ips
 	if str(ip) in ips:
 		ips.remove(str(ip))
 	userName = ""

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
			global images
			images.append(href)
			return href
def getPic(url):
	index = url.find("/" , url.find(".tv"))
	index2 = url.find("/",index+1)
	
	return getPicFromName(url[index+1:index2])
def getHomeLink(url):
	index = url.find(".tv/")
	index2 = url.find("/",index+5)
	rea = url[index+4:index2]
	global pop
	pop.append(rea)
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
def getResp(phrase):
	a = firebase.get(phrase,None)
	if a == None:
		return None
	keys = []
	for key in a:
		"""
		print "key: %s , value: %s" % (key, a[key])
		"""
		keys.append(key)
	return a[keys[0]]

def addUser(email,passW):
	users = eval(getResp("Users"))
	users.append(email)
	firebase.delete('Users',None)
	firebase.post("Users",str(users))
	b = eval(getResp("passwords"))
	b.append(passW)
	firebase.delete('passwords',None)
	firebase.post("passwords",str(b))
def isGood(user):
	users = eval(getResp("Users"))
	return user in users
def loginUser(user,passW):
	print "Logging In"
	users = eval(getResp("Users"))
	b = eval(getResp("passwords"))
	for i in range(0,len(users)):
		if users[i] == user:
			if b[i] == passW:
				return True
			else:
				return False
	return False
def getPass(user):
	print "Logging In"
	users = eval(getResp("Users"))
	b = eval(getResp("passwords"))
	for i in range(0,len(users)):
		if users[i] == user:
			return b[i]
	return ""
def addComic(email,comic):
	print "Logging In"
	users = eval(getResp("Users"))
	b = eval(getResp("Comics"))
	for i in range(0,len(users)):
		if users[i] == email:
			if comic not in b[i]:
				b[i].append(comic)
	firebase.delete('Comics',None)
	firebase.post("Comics",str(b))
def removeComic(email,comic):
	print "Logging In"
	users = eval(getResp("Users"))
	b = eval(getResp("Comics"))
	for i in range(0,len(users)):
		if users[i] == email:
			if comic in b[i]:
				b[i].remove(comic)
	firebase.delete('Comics',None)
	firebase.post("Comics",str(b))
def getMyComics(email):
	print "Logging In"
	users = eval(getResp("Users"))
	b = eval(getResp("Comics"))
	for i in range(0,len(users)):
		if users[i] == email:
			print "Moments"
			return b[i]
	print "Log"
def checkComicInList(email,com):
	print "Logging In"
	users = eval(getResp("Users"))
	b = eval(getResp("Comics"))
	for i in range(0,len(users)):
		if users[i] == email:
			print "Moments"
			if com in b[i]:
				return "yes"
			else:
				return "no"
	print "Log"
def setUserName(name):
    global userName 
    global myComics   # Needed to modify global copy of globvar
    userName = name
    myComics = getMyComics(name)
def setComicList(arr):
	global comicList
	comicList = []
	comicList = arr
def getNext(arr,iss,comic):
	if len(arr) == 0:
		iss = getIssuse(comic)
		issName = []
		for i in iss:
			issName.append(getIssueName(i))
		setComicList(issName)
	print "Enter Next"
	for i in range(0,len(arr)):
		print "Arr: "+str(arr[i])
		if str(arr[i]) == str(iss):
			if i < len(arr) - 1:
				return str(arr[i+1])
			else:
				return "no"
	return "no"
def getPrev(arr,iss):
	for i in range(0,len(arr)):
		if str(arr[i]) == str(iss):
			if i != 0:
				return str(arr[i-1])
			else:
				return "no"
	return "no"


#addUser("abirshukla1@gmail.com","aadi2247")
#print getIssueName("http://www.readcomics.net/harley-quinn/chapter-26")

#print getHomeLink("http://www.readcomics.tv/harley-quinn/chapter-26")

