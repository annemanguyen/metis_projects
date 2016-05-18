try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '15914510-OZu3367GY1Ucym1ZWiSeN31usiGhjKX63LZyBLsKX'
ACCESS_SECRET = 'Kcl75DUW1iKBE02x6C2wz6efDM0hmFT3e8NVdRsOjfso2'
CONSUMER_KEY = 'zSV7gDE1DoDziqKagRDxBXqoW'
CONSUMER_SECRET = 'gxEK5Kg1RqB6BkBNAmrKlXd8iVSkoNKvYKyl6pBt5adWpRwEtp'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

#specific user
#twitter_userstream = TwitterStream(auth=oauth, domain='accountability.twitter.com')

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

#get tweets in english including keyword
#iterator = twitter_stream.statuses.filter(track='Metis',language='en')

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 1000
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print json.dumps(tweet)  
    
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
    if tweet_count <= 0:
        break 

### save data: python twitter_streaming.py > twitter_stream_1000.txt