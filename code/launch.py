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
	return render_template("home.html",pop = pop,images = images)
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
	arr = scrape.crawlComicPages("http://www.readcomics.net/"+comic+"/chapter-"+issue+"/full")
	return render_template("comic.html",arr=arr)
"""
	arr = None
	arr = []
	arr = scrape.crawlComicPages("http://www.readcomics.net/the-flash-rebirth/chapter-1/full")
	return render_template("comic.html",arr=arr)

@app.route('/<movie>/')
def tester(movie):
	return render_template("test.html",movie=movie)
@app.route('/search',methods=['POST'])
def SearchMovie(names = [],links = [],search = None,imgs=[]):
	print "YO"
	names = []
	links = []
	imgs=[]
	search = ""
	search = request.form['search']
	links = scrape.getSolarSearch(str(search))
	for i in links:
		names.append(scrape.getNameFromLink(i))
	for name in names:
		if "www.solarmovie" in name:
			names.remove(name)
		else:	
			imgs.append(scrape.crawlImg(name))
	print imgs
	print names
	print "Done"
	return render_template("searchResults.html",names=names,links=links,imgs =imgs,search=search)



@app.route('/movie/<movie>/')
def hello(movie,emb = None, more=None,torr = None,imdb=None,imL = None,rotLink= None,rotRate=None,summary = None,streams = [],sol = None,relLinks = [],relNames = [],bef=None,imgRel = []):
	print "Homie"
	emb = ""
	emb = scrape.getTrailer(movie)
	print "Trailer Done"
	more = ""
	more = scrape.getMovieSearch(movie)
	print "Movie Seqrch Done"
	torr = ""
	torr = scrape.getTorrent(movie)
	print "Torrent Done"
	imdb = ""
	imdb = scrape.getRating(movie)
	imL = ""
	print "Rating"
	imL = scrape.getImdbLink(movie)
	print "IMDB"
	rotLink = ""
	rotRate = ""
	print "Rotten"
	rotLink = scrape.getRottenLink(movie)
	rotRate = scrape.getRottenRating(movie)
	print "Rotten"
	summary = ""
	summary = scrape.getSummary(imL)
	print "Summary!N"
	sol = ""
	sol = scrape.getSolarMovie(movie)
	streams = []
	print "sol "+sol
	streams = scrape.getStreamLink(sol)
	relNames= []
	relNames = scrape.getRelatedMoives(movie)
	relLinks = []
	print "Right Before"
	bef = ""
	for link in relNames:
		print link
		bef = ""
		bef = link.replace(" ","-")
		print bef
		relLinks.append("http://127.0.0.1:5000/"+bef+"/")
	imgRel = []
	for name in relNames:
		imgRel.append(scrape.crawlImg(name))
	return render_template("home.html",movie=movie,emb =emb,more=more,torr=torr,imdb = imdb,imL=imL,rotRate = rotRate,rotLink = rotLink,summary =summary,streams=streams,relNames = relNames, relLinks = relLinks,imgRel = imgRel)
"""
if __name__ == '__main__':
    app.run()
