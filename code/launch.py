from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from random import randint
import time
import scrape
import os
app = Flask(__name__)

@app.route('/')
def Home(popA = None, images = None,pop = None):
	"""popA = None
	popA = []
	images = None
	images = []
	pop = None
	pop = []
	popA = scrape.getPop()
	for i in popA:
		images.append(scrape.getPic(i))
		pop.append(scrape.getHomeLink(i))
	return render_template("home.html",pop = pop,images = images)
	"""
	return render_template("login.html")
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
def comicHome(comic,genre = None,iss=None, issName = None,status=None,image = None):
	status = None
	status = ""
	genre = None
	genre = ""
	iss = None
	iss = []
	issName = None
	issName = []
	comic = comic.replace(" ","-")
	iss = scrape.getIssuse(comic)
	for i in iss:
		issName.append(scrape.getIssueName(i))
	genre = scrape.getGenre(comic)
	status = scrape.getStatus(comic)
	comic = comic.replace("-"," ")
	comic = comic.title()
	image = None
	image = ""
	image = scrape.getPicFromName(comic)
	return render_template("comicHome.html",iss = iss, issName = issName, genre = genre, status = status,comic = comic,image = image)
@app.route('/<comic>/<issue>/')
def readComic(comic,issue,arr = None):
	comic = comic.replace(" ","-")
	arr = None
	arr = []
	arr = scrape.crawlComicPages("http://www.readcomics.tv/"+comic+"/chapter-"+issue+"/full")
	return render_template("comic.html",arr=arr)

if __name__ == '__main__':
    app.run()
