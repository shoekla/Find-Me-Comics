from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from random import randint
import time
import scrape
import os
import sendMail
app = Flask(__name__)
userN = ""
@app.route('/')
def Home(popA = None, images = None,pop = None,name = None):
	if str(request.remote_addr) not in scrape.ips:
		#print "Ips: "+scrape.ips
		return render_template("login.html")

	if scrape.userName != "":
		return redirect("/myComics")
	else:	
		return render_template("login.html")


@app.route('/popularComics')
def popluarComcis(popA = None, images = None,pop = None,name = None):
	if len(scrape.pop) != 0:
		return render_template("home.html",pop = scrape.pop,images = scrape.images,name=scrape.userName)
	popA = None
	popA = []
	name = None
	name = ""
	name = scrape.userName
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.getPop()
	for i in popA:
		images.append(scrape.getPic(i))
		pop.append(scrape.getHomeLink(i))
	for i in scrape.images:
		print "Image: "+i
	return render_template("home.html",pop = pop,images = images,name=name)

@app.route('/FindMeComicUser',methods=['POST'])
def signIn(email= None,passW=None):
	print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	passW = request.form['passW']
	scrape.setUserName(email)
	print "Sign2"
	if scrape.loginUser(email,passW):
		global userN
		userN = email
		scrape.addIp(str(request.remote_addr))
		#print "Ips: "+scrape.ips
		return redirect("/")
	else:
		return render_template("login.html",mess="Invalid Login Credentials")
@app.route('/AddComicUser',methods=['POST'])
def signUp(email= None,passW=None):
	print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	passW = request.form['passW']
	print "Sign2"
	if scrape.isGood(email):
		return render_template("login.html",mess="Email already In System :(")
	else:
		scrape.addUser(email,passW)
		return render_template("login.html",mess="You Were added! Please Sign in")
@app.route("/ip/")
def getip():
	return str(request.remote_addr)
@app.route('/emailUser',methods=['POST'])
def forgotEmail(email=None,passW=None):
	print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	if scrape.getPass(email) == "":
		return render_template("login.html",mess="Email not found :(")
	else:
		sendMail.sendEmailFromAbir("Password For Find Me Comics", "The password for your Find Me Comics Account is "+scrape.getPass(email)+".",email)
		return render_template("login.html",mess="Email sent with Password")
@app.route('/myComics')
def myComicHome(popA = None,images = None,pop = None,name=None):
	print "Enter Methid"
	if userN != "":
		popA = None
		popA = []
		name = None
		name = ""
		name = userN
		images = None
		images = []
		pop = None
		pop = []
		popA = scrape.getMyComics(name)
		print "One"
		for i in popA:
			images.append(scrape.getPicFromName(i.replace("-"," ").title()))
		print "Almost"
		return render_template("myComics.html",popA = popA,images=images)
	else:	
		return render_template("login.html")

@app.route('/addComic/<comic>/')
def addToMyC(comic,email = None):
	email = None
	email = ""
	email = scrape.userName
	comic = comic.replace(" ","-")
	scrape.addComic(email,comic)
	return redirect("/myComics")
@app.route('/removeComic/<comic>/')
def removeToMyC(comic,email = None):
	email = None
	email = ""
	email = scrape.userName
	comic = comic.replace(" ","-")
	scrape.removeComic(email,comic)
	return redirect("/myComics")


@app.route('/load')
def loadTem():
	return render_template("load.html")
@app.route('/',methods=['POST'])
def search(name =None,popA = None, images = None,pop = None):
	name = request.form['name']
	popA = None
	popA = []
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.searchComic(name)
	for i in popA:
		images.append(scrape.getPic(i))
		pop.append(scrape.getHomeLink(i))
	return render_template("searchResults.html",name=name,pop = pop,images=images)
@app.route('/test')
def testPage(s =None):
	s = None
	s = ""
	return render_template("test.html",s=s)

@app.route('/<comic>/')
def comicHome(comic,genre = None,iss=None, issName = None,status=None,image = None,comicName = None,com = None):
	if scrape.userName == "":
		return render_template("login.html")
	status = None
	status = ""
	genre = None
	genre = ""
	iss = None
	iss = []
	issName = None
	comicName = None
	comicName = ""
	com = None
	com = ""
	issName = []
	comic = comic.replace(" ","-")
	com = scrape.checkComicInList(scrape.userName,comic)
	iss = scrape.getIssuse(comic)
	for i in iss:
		issName.append(scrape.getIssueName(i))
	if len(issName) == 0:
		issName = scrape.comicList
	genre = scrape.getGenre(comic)
	genre = genre.replace(" ,",",")
	genre = genre.replace(",",", ")
	status = scrape.getStatus(comic)
	comicName = comic
	comic = comic.replace("-"," ")
	comic = comic.title()
	image = None
	image = ""
	image = scrape.getPicFromName(comic)
	scrape.setComicList(issName)
	for i in scrape.comicList:
		print "Comic List: "+i
	return render_template("comicHome.html",iss = iss, issName = issName, genre = genre, status = status,comic = comic,image = image,comicName = comicName,com = com)
@app.route('/<comic>/<issue>/')
def readComic(comic,issue,arr = None,name=None,nextB = None,prev = None):
	print "Issue Read: "+issue
	comic = comic.replace(" ","-")
	arr = None
	arr = []
	name = None
	name = ""
	nextB = None
	nextB = ""
	prev = None
	prev = ""
	print "Just Making Sure"
	nextB = scrape.getNext(scrape.comicList,issue,comic)
	print "Next Good"
	prev = scrape.getPrev(scrape.comicList,issue)
	print "Got Prev and Next"
	arr = scrape.crawlComicPages("http://www.readcomics.tv/"+comic+"/chapter-"+issue+"/full")
	print "Crawled Images"
	name = comic.replace("-"," ").title()
	return render_template("comic.html",arr=arr,issue=issue,comic=comic,name = name,nextB = nextB,prev = prev)
@app.route('/print/<comic>/<issue>/')
def printComic(comic,issue,arr = None,name=None):
	print "Issue Read: "+issue
	comic = comic.replace(" ","-")
	arr = None
	arr = []
	name = None
	name = ""
	arr = scrape.crawlComicPages("http://www.readcomics.tv/"+comic+"/chapter-"+issue+"/full")
	name = comic.replace("-"," ").title()
	return render_template("print.html",arr=arr,issue=issue,comic=comic,name = name)

@app.route('/logout/')
def logoutUser():
	scrape.logout(str(request.remote_addr))
	print "Ips: "+scrape.ips
	global userN 
	userN = ""
	return redirect("/")
if __name__ == '__main__':
	app.run()


