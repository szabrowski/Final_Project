## Your name: Scott Zabrowski
## The option you've chosen: Option 2

# Put import statements you expect to need here!

import unittest
import itertools
import collections
import tweepy
import twitter_info
import json
import sqlite3
import pprint
import requests


consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = "206_final_project_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

#print (api)

### CLASS TO GET DATA ON MOVIES - INSTANCE VARIABLES NEED WORK
### NEEDS TO HAVE A DICTIONARY INSERTED CONTAINING ONE MOVIE 

class Movie():

	def __init__(self, movie):
		self.movie_name = movie
		self.movie_data = {}
		#print (self.movie_data)
		self.movie_actors = []
		self.movie_director = []
		self.movie_IMDB_rating = []
		self.movie_Year = []
		self.movie_BoxOffice = []
		self.ID = []


	def __str__(self):
		#print ('I have found your data on %s' % (self.movie_name))
		return ('I have found your data on %s' % (self.movie_name))

	def get_movie_info(self):
		unique_id = 'OMDB_%s'%(self.movie_name)

		if unique_id in CACHE_DICTION:
			#print ('Using Cache data to get info about %s' (self.movie_name))
			json_load = CACHE_DICTION[unique_id]
		else:
			#print ('Getting data on %s' (self.movie_name))
			params = {'apikey': 'ee457035', 'format': 'json', 't': self.movie_name}
			api = requests.get('http://www.omdbapi.com/?', params = params)
			#print (api.status_code)
			json_load = json.loads(api.text)
			#print (json_load)
			#self.movie_data.append(json_load)
			self.movie_data[self.movie_name] = json_load
			pp = pprint.PrettyPrinter(indent=4)
			#pp.pprint(json_load)
			self.movie_actors.append(json_load['Actors'])
			#self.movie_director.append(json_load['Director'])
			self.movie_IMDB_rating.append(json_load['imdbRating'])
			self.movie_Year.append(json_load['Year'])
			self.movie_BoxOffice.append(json_load['BoxOffice'])
			self.movie_director.append(json_load['Director'])
			#print (self.movie_director)
			self.ID.append(json_load['imdbID'])
			# print (json_load['Actors'])
			# print (json_load['Director'])
			# print (json_load['imdbRating'])
			# print (json_load['Year'])
			# print (json_load['BoxOffice'])

		CACHE_DICTION[unique_id] = json_load
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return (json_load)


zzz = Movie('Inception')
print (zzz)
# def get_movie_info(self):
# 		params = {'apikey': 'ee457035', 'format': 'json', 't': self.movie_name}
# 		api = requests.get('http://www.omdbapi.com/?', params = params)
# 		#print (api.status_code)
# 		json_load = json.loads(api.text)
# 		#print (json_load)
# 		#self.movie_data.append(json_load)
# 		self.movie_data[self.movie_name] = json_load
# 		pp = pprint.PrettyPrinter(indent=4)
# 		#pp.pprint(json_load)
# 		self.movie_actors.append(json_load['Actors'])
# 		#self.movie_director.append(json_load['Director'])
# 		self.movie_IMDB_rating.append(json_load['imdbRating'])
# 		self.movie_Year.append(json_load['Year'])
# 		self.movie_BoxOffice.append(json_load['BoxOffice'])
# 		self.movie_director.append(json_load['Director'])
# 		#print (self.movie_director)
# 		self.ID.append(json_load['imdbID'])
# 		# print (json_load['Actors'])
# 		# print (json_load['Director'])
# 		# print (json_load['imdbRating'])
# 		# print (json_load['Year'])
# 		# print (json_load['BoxOffice'])
# 		return (json_load)

list_of_Movie_data = []
list_of_Movie_instances = []
movie_dict = ['Inception', 'Avatar', 'Forrest Gump']

for x in movie_dict:
	m = Movie(x)
	m.get_movie_info()
	x = Movie(x)
	#x.get_movie_info
	# print (m.movie_name)
	# print (x.get_movie_info)
	list_of_Movie_data.append(m.movie_data)
	#list_of_Movie_instances.append(x.movie_data)

#print (list_of_Movie_instances)

# f = Movie('Interstellar')
# f.get_movie_info()
# print (f.movie_actors)


#### GRAB TWITTER INFO FOR THE 3 DIRECTORS

def get_twitter_info(movie):
	lst = []
	unique_id = 'twitter_%s'%(movie)
	if unique_id in CACHE_DICTION:
		print ('Using cache data to find Tweets about %s' % (movie))
		lst = CACHE_DICTION[unique_id]
	else:
		print ('Getting data on Tweets about %s' % (movie))
		x = Movie(movie)
		x.get_movie_info()
		search = x.movie_director
		#print (search)
		#print (twitter_api)
		search_results = twitter_api.search(search)
		string = json.dumps(search_results)
		json_loader = json.loads(string)
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(json_loader)
		lst = json_loader
		#print (lst)

	CACHE_DICTION[unique_id] = lst
	f = open(CACHE_FNAME, 'w')
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return lst


lst_of_twitter_info = []
for x in movie_dict:
	ff = get_twitter_info(x)
	lst_of_twitter_info.append(ff)


# for x in list_of_Movie_data:
# 	for z in x:
# 		pp = pprint.PrettyPrinter(indent=4)
# 		pp.pprint(x[z])
# 	# movie_id.append(x['imdbID'])
# 	# title.append(x['Title'])
	# director.append(x['Director'])
	# num_languages.append(len(x['Language']))
	# IMDB_rating.append(x['imdbRating'])
	# print (x['Actors'])
	# box_office.append(x['BoxOffice'])
	# year.append(x['Year'])

### GRAB INFO FROM THE RETURNED OMDB AND TWITTER DATA
### NEED THIS INFO TO BE THE CORRECT 'TYPE' IN ORDER TO BE ACCEPTED BY THE DATABASE (I.E. TITLE IS A STRING/TEXT)

movie_id = [x[z]['imdbID'] for x in list_of_Movie_data for z in x] ## NEED TO CONVERT TO AN INTEGER
title = [x[z]['Title'] for x in list_of_Movie_data for z in x]
director = [x[z]['Director'] for x in list_of_Movie_data for z in x]
num_languages = [x[z]['Language'] for x in list_of_Movie_data for z in x] ## STILL NEED TO GET THE COUNT OF THESE, NOT A STRING OF THE LANGS OFFERED
IMDB_rating = [x[z]['imdbRating'] for x in list_of_Movie_data for z in x] # DOES THIS NEED TO BE AN INTEGER? IS IN A STRING NOW
lead_actor = [x[z]['Actors'] for x in list_of_Movie_data for z in x]    ## STILL NEED TO SPLIT THIS AND GET THE FIRST ACTOR
box_office = [x[z]['BoxOffice'] for x in list_of_Movie_data for z in x]
year = [x[z]['Year'] for x in list_of_Movie_data for z in x]

tups_of_movies = list(zip(movie_id, title, director, num_languages, IMDB_rating, lead_actor, box_office, year))


# print (tups_of_movies)
# # for x in lst_of_twitter_info:
# # 	for z in x['statuses']:
# # 		pp = pprint.PrettyPrinter(indent=4)
# # 		pp.pprint(z)
# 		#pp.pprint(z['entities'])


movie_in_tweet = [] ## Struggling here to get the movie that is used in the tweet. Do I have to get this from the beginning where I grab the tweets?

tweet_id = [z['id'] for x in lst_of_twitter_info for z in x['statuses']]
user_id = [z['user']['id'] for x in lst_of_twitter_info for z in x['statuses']]
text = [z['text'] for x in lst_of_twitter_info for z in x['statuses']]
tweet_favorites = [z['favorite_count'] for x in lst_of_twitter_info for z in x['statuses']]
tweet_retweets = [z['retweet_count'] for x in lst_of_twitter_info for z in x['statuses']]
user_name = [z['user']['screen_name'] for x in lst_of_twitter_info for z in x['statuses']]
user_total_favorites = [z['user']['favourites_count'] for x in lst_of_twitter_info for z in x['statuses']]
mentioned_users_id = [n['id'] for x in lst_of_twitter_info for z in x['statuses'] for n in z['entities']['user_mentions']]
#print (mentioned_users_id)
# print (tweet_retweets)
# print (text)



### ZIP THE DATA INTO TUPLES THAT REPRESENT EACH TWEET

tweets_of_directors = list(zip(tweet_id, text, user_id,tweet_favorites, tweet_retweets))

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

### CREATE TABLES AND INPUT THE DATA INTO THE CORRECT COLUMNS

cur.execute("DROP TABLE IF EXISTS Movies")
Movies_specs = "CREATE TABLE IF NOT EXISTS "
Movies_specs += "Movies (movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages TEXT, IMDB_rating TEXT, lead_actor TEXT, box_office TEXT, year TEXT)"
cur.execute(Movies_specs)

cur.execute("DROP TABLE IF EXISTS Tweets")
Tweets_specs = "CREATE TABLE IF NOT EXISTS "
Tweets_specs += "Tweets (tweet_id INTEGER PRIMARY KEY, text TEXT, user_id TEXT, favorites INTEGER, retweets INTEGER)"
cur.execute(Tweets_specs)

cur.execute("DROP TABLE IF EXISTS Users")
Users_specs = "CREATE TABLE IF NOT EXISTS "
Users_specs += "Users (user_id INTEGER PRIMARY KEY, user_name TEXT, num_favorites INTEGER)"
cur.execute(Users_specs)

state1 = "DELETE FROM Movies"
state2 = "DELETE FROM Tweets"
state3 = "DELETE FROM Users"

cur.execute(state1)
cur.execute(state2)
cur.execute(state3)
conn.commit()

tweet_insert_statement = 'INSERT INTO Tweets VALUES (?,?,?,?,?)'
for x in tweets_of_directors:
	try:
		cur.execute(tweet_insert_statement, x)
	except sqlite3.IntegrityError:
		pass
conn.commit()


movie_insert_statement = 'INSERT INTO Movies VALUES (?,?,?,?,?,?,?,?)'

for z in tups_of_movies:
	cur.execute(movie_insert_statement, z)

conn.commit()



### TESTS NEED TO BE BETTER

# Write your test cases here.
#print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class Tests(unittest.TestCase):
	def test_caching(self):
		x = open('SI206_cache', 'r').read()
		self.assertTrue('MOVIED_XYZ' in x)
	def test_Tweets(self):
		m = Tweets('Inception')
		self.assertTrue(len(m)>0)
	def test_Tweets2(self):
		m = Tweets('Inception')
		self.assertEqual(type(m),dict)
	def test_Movies1(self):
		m = Movies(movie = 'Inception')
		self.assertTrue(type(m), dict)
	def test_Movies2(self):
		m = Movies(director = 'Christopher Nolan').ratings
		self.assertEqual(type(m), list)
	def test_Movies3(self):
		m = Movies(director = 'Christopher Nolan').ratings
		self.assertTrue(len(m)>0)
	def test_Movies4(self):
		m = Movies(director = 'Christopher Nolan', movie = 'Inception').ratings
		self.assertTrue(len(m)>1)


#
## Remember to invoke all your tests...

# if __name__ == "__main__":
# 	unittest.main(verbosity=2)