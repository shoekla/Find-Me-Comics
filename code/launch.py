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

@app.route('/')
def Home(popA = None, images = None,pop = None,name = None):
	if scrape.userName != "":
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
		return render_template("home.html",pop = pop,images = images,name=name)
	else:	
		return render_template("login.html")
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
	if scrape.userName != "":
		popA = None
		popA = []
		name = None
		name = ""
		name = scrape.userName
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
def comicHome(comic,genre = None,iss=None, issName = None,status=None,image = None,comicName = None):
	status = None
	status = ""
	genre = None
	genre = ""
	iss = None
	iss = []
	issName = None
	comicName = None
	comicName = ""
	issName = []
	comic = comic.replace(" ","-")
	iss = scrape.getIssuse(comic)
	for i in iss:
		issName.append(scrape.getIssueName(i))
	genre = scrape.getGenre(comic)
	status = scrape.getStatus(comic)
	comicName = comic
	comic = comic.replace("-"," ")
	comic = comic.title()
	image = None
	image = ""
	image = scrape.getPicFromName(comic)
	return render_template("comicHome.html",iss = iss, issName = issName, genre = genre, status = status,comic = comic,image = image,comicName = comicName)
@app.route('/<comic>/<issue>/')
def readComic(comic,issue,arr = None):
	comic = comic.replace(" ","-")
	arr = None
	arr = []
	arr = scrape.crawlComicPages("http://www.readcomics.tv/"+comic+"/chapter-"+issue+"/full")
	return render_template("comic.html",arr=arr)

if __name__ == '__main__':
    app.run()
