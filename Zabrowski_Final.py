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
		return ('I have found your data on %s' % (self.movie_name))

	def get_movie_info(self):
		unique_id = 'OMDB_%s'%(self.movie_name)

		if unique_id in CACHE_DICTION:
			print ('Using Cache data to get info about %s' % (self.movie_name))
			print ('----------------------------------------')
			json_load = CACHE_DICTION[unique_id]
			self.movie_data[self.movie_name] = (json_load)
			self.movie_actors.append(json_load['Actors'])
			self.movie_IMDB_rating.append(json_load['imdbRating'])
			self.movie_Year.append(json_load['Year'])
			self.movie_BoxOffice.append(json_load['BoxOffice'])
			self.movie_director.append(json_load['Director'])
			self.ID.append(json_load['imdbID'])
		else:
			print ('Getting data on %s' % (self.movie_name))
			print ('----------------------------------------')
			params = {'apikey': 'ee457035', 'r': 'json', 't': self.movie_name}
			api = requests.get('http://www.omdbapi.com/?', params = params)
			json_load = json.loads(api.text)
			self.movie_data[self.movie_name] = (json_load)
			pp = pprint.PrettyPrinter(indent=4)
			#pp.pprint(json_load)
			self.movie_actors.append(json_load['Actors'])
			self.movie_IMDB_rating.append(json_load['imdbRating'])
			self.movie_Year.append(json_load['Year'])
			self.movie_BoxOffice.append(json_load['BoxOffice'])
			self.movie_director.append(json_load['Director'])
			self.ID.append(json_load['imdbID'])

		CACHE_DICTION[unique_id] = json_load
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return (json_load)



list_of_Movie_data = []
movie_dict = ['Inception', 'Avatar', 'Forrest Gump']

for x in movie_dict:
	m = Movie(x)
	m.get_movie_info()
	list_of_Movie_data.append(m.movie_data)



#### GRAB TWITTER INFO FOR THE 3 DIRECTORS

def get_twitter_info(movie):
	lst = []
	unique_id = 'twitter_%s'%(movie)
	if unique_id in CACHE_DICTION:
		print ('Using cache data to find Tweets about %s' % (movie))
		print ('----------------------------------------')
		lst = CACHE_DICTION[unique_id]
	else:
		print ('Getting data on Tweets about %s' % (movie))
		print ('----------------------------------------')
		x = Movie(movie)
		x.get_movie_info()
		search = x.movie_director
		#print (search)
		#print (twitter_api)
		search_results = twitter_api.search(search)
		string = json.dumps(search_results)
		json_loader = json.loads(string)
		pp = pprint.PrettyPrinter(indent=4)
		#pp.pprint(json_loader)
		lst = json_loader
		#print (lst)

	CACHE_DICTION[unique_id] = lst
	f = open(CACHE_FNAME, 'w')
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return lst

pp = pprint.PrettyPrinter(indent=4)

lst_of_twitter_info = []
# user_movie_mention = []
# mentioned_user_movie_mention = []
movie_mentions_list = []


for x in movie_dict:
	user_movie_mention = []
	mentioned_user_movie_mention = []
	ff = get_twitter_info(x)
	lst_of_twitter_info.append(ff)
	for z in ff['statuses']:
		#pp.pprint(z['text'])
		user_movie_mention.append(z['text'])
		for n in z['entities']['user_mentions']:
			mentioned_user_movie_mention.append(n['id'])
	movie_mentions_list.append([x]*len(user_movie_mention + mentioned_user_movie_mention))

mention_movie = []
for x in movie_mentions_list:
	for z in x:
		mention_movie.append((z))


#pp.pprint(lst_of_twitter_info)

#print (mention_movie)

### GRAB INFO FROM THE RETURNED OMDB AND TWITTER DATA
### NEED THIS INFO TO BE THE CORRECT 'TYPE' IN ORDER TO BE ACCEPTED BY THE DATABASE (I.E. TITLE IS A STRING/TEXT)

movie_id = [x[z]['imdbID'] for x in list_of_Movie_data for z in x]
title = [x[z]['Title'] for x in list_of_Movie_data for z in x]
director = [x[z]['Director'] for x in list_of_Movie_data for z in x]
languages = [x[z]['Language'] for x in list_of_Movie_data for z in x]
num_languages = [len(m.split(', ')) for m in languages]
IMDB_rating = [x[z]['imdbRating'] for x in list_of_Movie_data for z in x]
actors = [x[z]['Actors'] for x in list_of_Movie_data for z in x]
lead_actor = [(x.split(', '))[0] for x in actors]
box_office = [x[z]['BoxOffice'] for x in list_of_Movie_data for z in x]
year = [x[z]['Year'] for x in list_of_Movie_data for z in x]
tweet_id = [z['id'] for x in lst_of_twitter_info for z in x['statuses']]
user_id = [z['user']['id'] for x in lst_of_twitter_info for z in x['statuses']]
text = [z['text'] for x in lst_of_twitter_info for z in x['statuses']]
tweet_favorites = [z['favorite_count'] for x in lst_of_twitter_info for z in x['statuses']]
tweet_retweets = [z['retweet_count'] for x in lst_of_twitter_info for z in x['statuses']]
user_name = [z['user']['screen_name'] for x in lst_of_twitter_info for z in x['statuses']]
user_total_favorites = [z['user']['favourites_count'] for x in lst_of_twitter_info for z in x['statuses']]
mentioned_users_id = [n['id'] for x in lst_of_twitter_info for z in x['statuses'] for n in z['entities']['user_mentions']]
mentioned_users_screen_name = [n['screen_name'] for x in lst_of_twitter_info for z in x['statuses'] for n in z['entities']['user_mentions']]
mentioned_users_favs = [twitter_api.get_user(x)['favourites_count'] for x in mentioned_users_id]
#print (mentioned_users_favs)
users_total = mentioned_users_id + user_id
screen_name_total = mentioned_users_screen_name + user_id
total_user_favs = mentioned_users_favs + user_total_favorites

# print (len(mentioned_users_id))
### ZIP THE DATA INTO TUPLES THAT REPRESENT EACH TWEET

tups_of_movies = list(zip(movie_id, title, director, num_languages, IMDB_rating, lead_actor, box_office, year))
tweets_of_directors = list(zip(tweet_id, text, user_id,tweet_favorites, tweet_retweets, mention_movie))
tup_of_users = list(zip(users_total, screen_name_total, total_user_favs))

### CREATE DATABASE

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

### CREATE TABLES AND INPUT THE DATA INTO THE CORRECT COLUMNS

cur.execute("DROP TABLE IF EXISTS Movies")
Movies_specs = "CREATE TABLE IF NOT EXISTS "
Movies_specs += "Movies (movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages TEXT, IMDB_rating TEXT, lead_actor TEXT, box_office TEXT, year TEXT)"
cur.execute(Movies_specs)

cur.execute("DROP TABLE IF EXISTS Tweets")
Tweets_specs = "CREATE TABLE IF NOT EXISTS "
Tweets_specs += "Tweets (tweet_id INTEGER PRIMARY KEY, text TEXT, user_id TEXT, favorites INTEGER, retweets INTEGER, mention_movie TEXT)"
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

tweet_insert_statement = 'INSERT INTO Tweets VALUES (?,?,?,?,?, ?)'
for x in tweets_of_directors:
	try:
		cur.execute(tweet_insert_statement, x)
	except sqlite3.IntegrityError:
		pass
conn.commit()


movie_insert_statement = 'INSERT INTO Movies VALUES (?,?,?,?,?,?,?,?)'

for z in tups_of_movies:
	cur.execute(movie_insert_statement, z)

user_insert_statement = 'INSERT INTO Users VALUES (?,?,?)'

for m in tup_of_users:
	try:
		cur.execute(user_insert_statement, m)
	except sqlite3.IntegrityError:
		pass
		
conn.commit()

### ACCESS DATABASE AND ANALYZE IT. THEN WRITE IT TO A TEXT FILE ###
query_analysis = 'SELECT IMDB_rating FROM Movies'
high_rating = list(cur.execute(query_analysis))

total_combined_rate = list(itertools.accumulate(high_rating))
tup_ratings = total_combined_rate[-1]
#print(tup_ratings)

query5 = 'SELECT Text, retweets FROM Tweets'
high_favs = list(cur.execute(query5))

query6 = 'SELECT Movies.title, Tweets.favorites FROM Movies INNER JOIN Tweets ON instr(Movies.title, Tweets.mention_movie) WHERE Tweets.favorites>5'
movies_w_high_favs = list(cur.execute(query6))

query7 = 'SELECT Movies.title, Movies.box_office FROM Movies'
movies_box_office = list(cur.execute(query7))
m = sorted(movies_box_office, key = lambda x:x[-1])
#print (m)

query8 = 'SELECT Movies.title, Tweets.favorites FROM Movies INNER JOIN Tweets ON instr(Movies.title, Tweets.mention_movie)'
favs_per_movie = list(cur.execute(query8))

total_favorites = 0

for x in favs_per_movie:
	total_favorites += int(x[1])

dict_favs = {x[0]:x[1] for x in movies_w_high_favs}  ### WOULD BE MORE USEFUL WITH MORE MOVIES



summary_file = '%s_OMDB&Tweet_Data_4-25-16.txt' % (movie_dict[0]+"_"+movie_dict[1]+"_"+movie_dict[2])
w = open(summary_file, 'w')
w.write('Movies with more than 5 favorites: ' + str(dict_favs) + "  ")
w.write('Total Favorites for these movie: ' + str(total_favorites) + "  ")
w.write('Movies sorted by box office: ' + str(m) + " ")
w.write('All Ratings ' + str(tup_ratings) + " ")
w.close()

### TESTS NEED TO BE BETTER

# Write your test cases here.
#print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class Tests(unittest.TestCase):
	def test_caching(self):
		x = open('206_final_project_cache.json', 'r').read()
		self.assertTrue('OMDB_Inception' in x)
	def test_Tweets(self):
		m = get_twitter_info('Inception')
		self.assertTrue(len(m)>0)
	def test_Movies1(self):
		m = Movie('Inception').get_movie_info()
		self.assertEqual(type(m),dict)
	def test_Movies2(self):
		m = Movie('Inception').__str__()
		self.assertTrue(type(m), str)
	def test_Movies3(self):
		self.assertEqual(len(IMDB_rating),len(title))
	def test_Movies4(self):
		m = Movie('Inception').__str__()
		self.assertEqual(m, 'I have found your data on Inception')
	def test_Tup(self):
		self.assertEqual(type(tup_ratings), tuple)
	def test_tups_movies(self):
		self.assertEqual(len(tups_of_movies), 3)
## Remember to invoke all your tests...

if __name__ == "__main__":
	unittest.main(verbosity=2)