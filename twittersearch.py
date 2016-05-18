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

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)
            
# Search for latest tweets about "#food"
#print json.dumps(twitter.search.tweets(q='#food', result_type='recent', lang='en', count=10), indent=4)

#search for trends in a given place (nyc)
#nyc_trends = twitter.trends.place(_id = 2459115)
#print json.dumps(nyc_trends, indent=4)

# Get a list of followers of a particular user
#print twitter.followers.ids(screen_name="accountability")

# Get a particular user's timeline (up to 3,200 of his/her most recent tweets)
print json.dumps(twitter.statuses.user_timeline(screen_name="accountability"), indent=4)

# rate status
print json.dumps(twitter.application.rate_limit_status(), indent=4)