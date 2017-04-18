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
		print ('I have found your data on %s' % (self.movie_name))
		return ('I have found your data on %s' % (self.movie_name))


	def get_movie_info(self):
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
		return (json_load)


list_of_Movie_data = []
list_of_Movie_instances = []
movie_dict = ['Inception', 'Interstellar', 'Batman Begins']

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



def get_twitter_info(movie):
	lst = []
	if movie in CACHE_DICTION:
		print ('Using cache data to find Tweets about %s' % (movie))
		lst = CACHE_DICTION[movie]
	else:
		print ('Getting data on Tweets about %s' % (movie))
		x = Movie(movie)
		x.get_movie_info()
		search = x.movie_director
		#print (search)
		#print (twitter_api)
		search_results = twitter_api.user_timeline(search, count = 25, page = 1)
		string = json.dumps(search_results)
		json_loader = json.loads(string)
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(json_loader)
		lst = json_loader
		#print (lst)

	CACHE_DICTION[movie] = lst
	f = open(CACHE_FNAME, 'w')
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return lst


for x in movie_dict:
	get_twitter_info(x)



# conn = sqlite3.connect('final_project.db')
# cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS Movies')
# cur.execute('DROP TABLE IF EXISTS Tweets')
# #cur.execute('DROP TABLE IF EXISTS Users')

# Movies_specs = 'CREATE TABLE IF NOT EXISTS '
# Movies_specs += 'Movies (movie_id INTEGER PRIMARY KEY, title TEXT, director TEXT, num_languages INTEGER, IMDB_rating INTEGER, lead_actor TEXT, box_office INTEGER, year INTEGER)'
# cur.execute(Movies_specs)

# Tweets_specs = 'CREATE TABLE IF NOT EXISTS '
# Tweets_specs =+ 'Tweets (tweet_id INTEGER PRIMARY KEY, text TEXT, user_id TEXT, movie_id INTEGER, favorites INTEGER, retweets INTEGER)'
# cur.execute(Tweets_specs)

# Users_specs = 'CREATE TABLE IF NOT EXISTS '
# Users_specs += 'Users (user_id INTEGER PRIMARY KEY, user_name TEXT, num_favorites INTEGER)'
# cur.execute(Users_specs)


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



## Remember to invoke all your tests...

# if __name__ == "__main__":
# 	unittest.main(verbosity=2)