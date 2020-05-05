from flask import Flask,jsonify, request, render_template, redirect, url_for, abort
import requests
from feedgen.feed import FeedGenerator
from flask import make_response
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

def ERRORFEED(FEED):
	ent = FEED.add_entry()
	ent.title("Error Title")
	ent.link(href="error.com")
	ent.description("This is the default feed item when nothing shows")
	ent.guid("1234",permalink=False)
	ent.author(name="Error-man", email="error@error.com")
	ent.pubDate("Mon, 14 Feb 2011 00:09:04 +0200")


#post_id --> id and comm_name --> community
def PostToResponse(post, feed):
	ent = feed.add_entry()
	ent.title(post['post_title'])
	ent.link(href="http://127.0.0.1:8000/r/" +str(post['comm_name'])+"/posts/"+str(post['post_id'])+"/comments")
	ent.description(post['post_body'])
	ent.guid(str(post['post_id']),permalink=False)
	ent.author(name="user id: " + str(post['post_id']), email="N/A")
	ent.pubDate(post['date'] + " +0200")


def GenerateFeed(community):
	fg = FeedGenerator()

	fg.description("This is for the most recent posts of the " + community + " community")
	if community == "all" :
		fg.link(href="http://127.0.0.1:9000/r/all/")
	else: 	
		fg.link(href="http://127.0.0.1:9000/r/"+community+"/posts/")
	return fg

@app.route('/RSS')
def RSSHome():
	return 'This is the RSS Home Page'

@app.route('/RSS/<community>/recent')
def RSSCommunityRecent(community):
	fg = GenerateFeed(community);
	fg.title("25 Recent Posts for: " + community)
	res = requests.get("http://127.0.0.1:8000/Vote", json={"command": "community", "comm_name":community})
	if res.ok != True :
		print('Error: Request Not Found!')
		return 'ERROR: Request Not Found!'
	resjson = res.json()
	for post in resjson['posts']:
		print post['post_title']
		PostToResponse(post, fg)
	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response	

@app.route('/RSS/recent')
def RSSRecent():
	fg = GeneratedFeed('all')
	fg.title("25 Recent Posts")
	res = requests.get("http://127.0.0.1:8000/Vote", json={"command": "recent"})
	if res.ok != True :
		print('Error: Request Not Found!')
		return 'ERROR: Request Not Found!'
	resjson = res.json()
	for post in resjson['posts']:
		print post['post_title']
		PostToResponse(post, fg)
	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response	

@app.route('/RSS/<community>/top')
def RSSCommunityTop(community):
	fg = GenerateFeed(community);
	fg.title("Top 25 Posts for: " + community)
	res = requests.get("http://127.0.0.1:8000/Vote", json={"command": "community", "comm_name":community})
	if res.ok != True :
		print('Error: Request Not Found!')
		return 'ERROR: Request Not Found!'
	resjson = res.json()
	for post in resjson['posts']:
		print post['post_title']
		PostToResponse(post, fg)
	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response	


@app.route('/RSS/top')
def RSSTop():
	fg = GenerateFeed('all');
	fg.title("Top 25 Posts!")
	res = requests.get("http://127.0.0.1:8000/Vote", json={"command": "top"})
	if res.ok != True :
		print('Error: Request Not Found!')
		return 'ERROR: Request Not Found!'
	resjson = res.json()
	for post in resjson['posts']:
		print post['post_title']
		PostToResponse(post, fg)
	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response	

@app.route('/RSS/hot')
def RSSHot():
	fg = GenerateFeed('all');
	res = requests.get("http://127.0.0.1:8000/Vote", json={"command": "hot"})
	if res.ok != True :
		print('Error: Request Not Found!')
		return 'ERROR: Request Not Found!'
	resjson = res.json()
	for post in resjson['posts']:
		print post['post_title']
		PostToResponse(post, fg)
	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response	

@app.route('/RSS/all')
def RSSAll():
	fg = GenerateFeed('all');
	fg.title("Test RSS for All Posts!")
	res = requests.get("http://127.0.0.1:8000/r/all")
	if res.ok != True :
		print('Error: Request Not Found!')
		return 'ERROR: Request Not Found!'
	resjson = res.json()
	for post in resjson['posts']:
		print post['post_title']
		PostToResponse(post, fg)
	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response	

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=9000)
