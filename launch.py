from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from random import randint
import time
import scrape
import os
#import sendMail
app = Flask(__name__)
@app.route('/')
def Home():
	return render_template("login.html")

@app.route('/FindMeComicUser',methods=['POST'])
def signIn(email= None,passW=None,popA = None,images = None,pop = None,name=None):
	#print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	email = email.strip()
	passW = request.form['passW']
	passW = passW.strip()
	#print "Sign2"
	if scrape.loginUser(email,passW):
		#print "Ips: "+scrape.ips
		popA = None
		popA = []
		name = None
		name = ""
		name = email
		images = None
		images = []
		pop = None
		pop = []
		popA = scrape.getMyComics(name)
		#print "One"
		for i in popA:
			images.append(scrape.getPicFromName(i.replace("-"," ").title()))
		#print "Almost"
		return render_template("myComics.html",popA = popA,images=images,name = name)
	else:
		return render_template("login.html",mess="Invalid Login Credentials")
@app.route('/search/',methods=['POST'])
def search(name =None,popA = None, images = None,pop = None,user = None):
	name = request.form['name']
	popA = None
	popA = []
	user = None
	user = ""
	user = request.form['user']
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.searchComic(name)
	for i in popA:
		images.append(scrape.getPic(i))
		pop.append(scrape.getHomeLink(i))
	return render_template("searchResults.html",name=name,pop = pop,images=images,user = user)



@app.route('/<comic>/',methods=['POST'])
def comicHome(comic,genre = None,iss=None, issName = None,status=None,image = None,comicName = None,com = None,name = None):
	try:
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
		name = None
		name = ""
		name = request.form['user']
		com = scrape.checkComicInList(name,comic)
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
		return render_template("comicHome.html",iss = iss, issName = issName, genre = genre, status = status,comic = comic,image = image,
			comicName = comicName,com = com,name = name)
	except:
		comic = comic.replace("-"," ").title()
		name = request.form['user']
		return render_template("error.html",comic = comic,name = name)
@app.route('/<comic>/')
def loginInSave(comic):
	return render_template("loginSave.html",comic=comic)
@app.route('/FindMeComicUser/Save/',methods=['POST'])
def loginBackendSave(email= None,passW=None,genre = None,iss=None, issName = None,status=None,image = None,comicName = None,com = None,name = None,comic = None):
	#print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	email = email.strip()
	passW = request.form['passW']
	passW = passW.strip()
	name = ""
	#print "Sign2"
	if scrape.loginUser(email,passW):
		try:
			print "1"
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
			print "2"
			comic = None
			comic = request.form['comic']
			comic = comic.replace(" ","-")
			name = None
			name = ""
			name = email
			print "3"
			com = scrape.checkComicInList(name,comic)
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
			return render_template("comicHome.html",iss = iss, issName = issName, genre = genre, status = status,comic = comic,image = image,
				comicName = comicName,com = com,name = name)
		except:
			comic = comic.replace("-"," ").title()
			name = request.form['user']
			return render_template("error.html",comic = comic,name = name)
	else:
		return render_template("loginSave.html",mess="Invalid Login Credentials")


@app.route('/myComics',methods=['POST'])
def myComicHome(popA = None,images = None,pop = None,name=None):
	#print "Enter Methid"
	popA = None
	popA = []
	name = None
	name = ""
	name = request.form['user']
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.getMyComics(name)
	#print "One"
	for i in popA:
		images.append(scrape.getPicFromName(i.replace("-"," ").title()))
	#print "Almost"
	return render_template("myComics.html",popA = popA,images=images,name = name)
@app.route('/myComics')
def notady():
	return render_template("login.html")
@app.route('/popularComics',methods=['POST'])
def popluarComcis(popA = None, images = None,pop = None,name = None):
	name = None
	name = ""
	name = request.form['user']
	popA = None
	popA = []
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.getPop()
	for i in popA:
		images.append(scrape.getPic(i))
		pop.append(scrape.getHomeLink(i))
	return render_template("home.html",pop = pop,images = images,name=name)
@app.route('/popularComics')
def ntoda():
	return render_template("login.html")
@app.route('/AddComicUser',methods=['POST'])
def signUp(email= None,passW=None):
	#print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	email = email.strip()
	passW = request.form['passW']
	passW = passW.strip()
	#print "Sign2"
	if scrape.isGood(email):
		return render_template("login.html",mess="Email already In System :(")
	else:
		scrape.addUser(email,passW)
		return render_template("login.html",mess="You Were added! Please Sign in")
@app.route('/removeComic/<comic>/',methods=['POST'])
def removeToMyC(comic,email = None,popA = None,images = None,pop = None):
	email = None
	email = ""
	email = request.form['user']
	comic = comic.replace(" ","-")
	scrape.removeComic(email,comic)
	#print "Enter Methid"
	popA = None
	popA = []
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.getMyComics(email)
	#print "One"
	for i in popA:
		images.append(scrape.getPicFromName(i.replace("-"," ").title()))
	#print "Almost"
	return render_template("myComics.html",popA = popA,images=images,name = email)

@app.route('/emailUser',methods=['POST'])
def forgotEmail(email=None,passW=None):
	#print "Sign"
	email = None
	passW = None
	email = ""
	passW = ""
	email = request.form['email']
	email = email.strip()
	passW = scrape.getPass(email)
	if passW == "":
		return render_template("login.html",mess="Email not found :(")
	else:
		print "Sending mail"
		scrape.sendEmailForPass(passW,email)
		print "Ok"
		return render_template("login.html",mess="Email sent with Password")
@app.route('/print/<comic>/<issue>/')
def printComic(comic,issue,arr = None,name=None):
	#print "Issue Read: "+issue
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
	return redirect("/")

@app.route('/addComic/<comic>/',methods=['POST'])
def addToMyC(comic,email = None,popA = None,images = None,pop = None):
	email = None
	email = ""
	email = request.form['user']
	comic = comic.replace(" ","-")
	scrape.addComic(email,comic)
	#print "Enter Methid"
	popA = None
	popA = []
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.getMyComics(email)
	#print "One"
	for i in popA:
		images.append(scrape.getPicFromName(i.replace("-"," ").title()))
	#print "Almost"
	return render_template("myComics.html",popA = popA,images=images,name = email)

@app.route('/t')
def testes():
	return render_template("test.html")

@app.route('/<comic>/<issue>/',methods=['POST'])
def readComic(comic,issue,arr = None,name=None,nextB = None,prev = None,user = None):
	#print "Issue Read: "+issue
	comic = comic.replace(" ","-")
	arr = None
	arr = []
	name = None
	name = ""
	nextB = None
	nextB = ""
	prev = None
	prev = ""
	user = None
	user = ""
	user = request.form['user']
	#print "Just Making Sure"
	nextB = scrape.getNext(scrape.comicList,issue,comic)
	#print "Next Good"
	prev = scrape.getPrev(scrape.comicList,issue)
	#print "Got Prev and Next"
	arr = scrape.crawlComicPages("http://www.readcomics.tv/"+comic+"/chapter-"+issue+"/full")
	#print "Crawled Images"
	name = comic.replace("-"," ").title()
	return render_template("comic.html",arr=arr,issue=issue,comic=comic,name = name,nextB = nextB,prev = prev,user=user)


@app.route('/recomendComic/<comic>/',methods=['POST'])
def recoComic(comic, rec=None,genre = None,iss=None, issName = None,status=None,image = None,comicName = None,com = None,name = None):
	name = None
	name = ""
	name = request.form['user']
	rec = None
	rec = ""
	rec = request.form['recName']
	scrape.sendEmailForRec(comic,name,rec)
	try:
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
		com = scrape.checkComicInList(name,comic)
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
		return render_template("comicHome.html",iss = iss, issName = issName, genre = genre, status = status,comic = comic,image = image,
			comicName = comicName,com = com,name = name,mess="Comic Email Sent!")
	except:
		comic = comic.replace("-"," ").title()
		name = request.form['user']
		return render_template("error.html",comic = comic,name = name)

if __name__ == '__main__':
	app.run()


