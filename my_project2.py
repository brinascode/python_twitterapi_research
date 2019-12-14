import spacy
import tweepy
import nltk
import spacy
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# The twitter handles we will generate our corpus from
twitter_handles = ["SaulOven",
			"sequoiacallahan",
			"hunterwagenaar",
			"KarishmaS26",
			"Jordan_DidThat",
			"e_meldao",
			"Deanna_Gowland",
			"BradDeMers",
			"MillsMallery",
			"breaira_sue",
			"umaramesh212",
			"helenrottier",
			"keithlnagy",
			"realBadea",
			"RonfromAK",
			"valeriesheehe",
			"KeanaParedes",
			"dougherty_chloe",
			"alexisxxvii",
			"SydneRae__",
            "teresaanguyenn_"]

test_handles = ["booboolafool",
			"Hannah_Alexis98",
			"kamistew",
			"ConnorSkilly",
			"adnanaziz10",
			"sadotson",
			"rryleekelly"]


# Creating our different corpora using these functions: Right now its synced with the test handles and corpus

def append_to_corpus(user):
    timeline_corpus = api.user_timeline(user, page=1)
    tweet_text = ""

    for tweet in timeline_corpus:
        tweet_text = tweet_text + tweet.text

    print(tweet_text)
    with open("test_corpus.txt", "a") as output:
         output.writelines(tweet_text)


def create_corpus(handle_list):
    for handle in handle_list:
        append_to_corpus(handle)

# create_corpus(test_handles)

# Spacy is trained with corpus using Spacy-NER-annotator tool -- so no steps here


# Getting a specific tweet:
tweet = api.get_status("1204134701994254336", tweet_mode="extended")


# Detecting if one of our entities in a tweet
# Place the path to the annotator here
college_needs_model = spacy.load(
    "") #Change this to absolute path to the model


entities = {
			"Food": [0.0, 0.0, []],  # Mean usage, sentiment, day of week
			"Product": [0.0, 0.0, []],
			"Money": [0.0, 0.0, []],
			"Justice": [0.0, 0.0, []],
			"Love": [0.0, 0.0, []],
			"Help": [0.0, 0.0, []],
			"Entertainment": [0.0, 0.0, []],
			"Clothing": [0.0, 0.0, []],
			"shopping": [0.0, 0.0, []],
			"Work": [0.0, 0.0, []]}


def get_tweets(user_list):
	for user in user_list:
		user_status_list = api.user_timeline(user, page=1)
		for tweet in user_status_list:
    		# Counting how many times an entity is detected
			# Feeding data into the model to get our named entities```
			print(tweet.text)
			doc = college_needs_model(tweet.text)
			for ent in doc.ents:
				entities[ent.label_][0] += 1
				print(entities[ent.label_][0])
    

   			# Calculating the sentiment for each entity
				from textblob import TextBlob
				tb = TextBlob(tweet.text)  # more neediness
				sentiment = tb.sentiment.polarity
				entities[ent.label_][1] += sentiment  # Then divide again to do the mean

			# Calculating the day # Later we pick the most common day
				import datetime
				date = datetime.date
				tweet_date_converted = (date.fromisoformat(str(tweet.created_at)[:10]))
				weekday = date(tweet_date_converted.year, tweet_date_converted.month,
				               tweet_date_converted.day).isoweekday()
				entities[ent.label_][2].append(weekday)

	# Next: we get the mean of the sentiments => divide the sum which is entities[ent][1] by number of occurences entities[ent][0]
	for ent in entities:
		if entities[ent][0] != 0:
			entities[ent][1] = entities[ent][1]/entities[ent][0]
	print (entities)
	
   
def plot_graph():
	import matplotlib.pyplot as plt
	entitiesList = [] # What it looks like entitiesList = ["Food","Product","Money","Justice","Love","Help","Entertainment","Clothing","shopping","Work"]
	entRank =[]
	entSentiment = []

	# Preparing our data
	for ent in entities:
		entitiesList.append(ent)
		entRank.append(entities[ent][0])
		entSentiment.append(entities[ent][1])
	print(entitiesList)
	print(entRank)

    # Ranking entity usage
	plt.title("Most common entities")
	plt.bar(entitiesList,entRank)
	plt.show()

	# Arithmetic Mean of Sentiments attached to these entities
	plt.plot(entitiesList, entSentiment)
	plt.ylabel("Sentiment Polarity")
	plt.xlabel("Entities")
	plt.title("Mean sentiment polarity for each entity")
	plt.show()
 
	# Top days for each entity
	
 
	# ["Food","Product","Money","Justice","Love","Help","Entertainment","Clothing","shopping","Work"]
 
	entityList2 = []
	mostDayForEnt =[] # Added an extra spot cause we dont have day 0
	for ent in entities:
		entityList2.append(ent)
		daysList = entities[ent][2]
		# Counting the occurrences of days
		days = {
					"Mon": 0,  # Mean usage, sentiment, day of week
					"Tue": 0,
					"Wed": 0,
					"Thu": 0,
					"Fri": 0,
					"Sat": 0,
					"Sun": 0  }
		days["Mon"] = daysList.count(1)
		days["Tue"] = daysList.count(2)
		days["Wed"] = daysList.count(3)
		days["Thu"] = daysList.count(4)
		days["Fri"] = daysList.count(5)
		days["Sat"] = daysList.count(6)
		days["Sun"] = daysList.count(7)
			
		highestCount = max(days["Mon"],days["Tue"],days["Wed"],days["Thu"],days["Fri"],days["Sat"],days["Sun"]) # Remember this is the 'count' value
		print("Highest count is")
		print(highestCount)
		toAppend = "No day"
		for day in days: # We find the day that the 'count' value corresponds to
			if days[day] == highestCount:
				toAppend = day
				print("Day that matches count is")
				print(day)
		mostDayForEnt.append(toAppend)
		print("Printing MOst Day for ent")
		print(mostDayForEnt)

	plt.plot(entityList2,mostDayForEnt)
	plt.ylabel("Days of the week")
	plt.xlabel("Entities")
	plt.title("Entity rank by day")
	plt.show()




get_tweets(["booboolafool",
			"Hannah_Alexis98",
			"kamistew",
			"ConnorSkilly",
			"adnanaziz10",
			"sadotson",
			"rryleekelly"])
plot_graph()


# What I want to report on: entity + polarity + day of the week 
# But how do I detect a "need"?? --> well you aren't really ...

# Seems like API is sending me a universal time stamp! Why does it show correctly on site though? Maybe to 
# help us by giving us the GMT time so that we can use that time accordingly and convert it to our country's own time.
# Since our tweets come from all over the US, we will just subtract a day?? 
# But then it gets complicated. Let's just take the GMT time and account for what that could mean --> a margin of error + or -
# A lot of error margins etc...y
# Disclaimers --> very arbitrart
'''

# Performing sentiment analysis --> to determine the neediness of the tweet
def detect_need(tweet): 
	# or should it be close to entity? ==> for a more complex upgrade later...
	score = 0  # The total is 
	
	ineed_index = tweet.full_text.find("I need")
	iwant_index = tweet.full_text.find("I want")
	need_index = tweet.full_text.find("need")
	want_index = tweet.full_text.find("want")
	
	if(ineed_index or iwant_index or need_index or want_index > -1):
		return True
	else:
		return False
	
    		
def find_sentiment(tweet):
	from textblob import TextBlob
	tb = TextBlob(tweet.full_text) # more neediness
	sentiment = tb.sentiment.polarity
	return (sentiment)

def find_weekday(tweet):
	 import datetime 
	 date = datetime.date
	 tweet_date_converted = (date.fromisoformat(str(tweet.created_at)[:10]))
	 weekday = date(tweet_date_converted.year, tweet_date_converted.month, tweet_date_converted.day).isoweekday()
	 return (weekday)
	 # Mon => 1, Sun => 7



with open("output.txt","w") as tweet_output:
    tweet_output.writelines(tweet) 

Status Object:
	- status.text
	- status.full_text
	- status.id_str or  status.id

Tweepy stuff:
    - A tweet in the API lingo is also called a Status Object. Contains extra info such as text, retweets, liked etc
    - api.user_timeline(user,page=1) --> Returns the most recent 20 statuses posted by that user handle
    - Status.text is the text content of the tweet that we care about
    - tweet.user --> Gives you the user object who posted that tweet
'''
