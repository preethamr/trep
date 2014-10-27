import access
import datetime
import math
import score
import time
import tweepy
from operator import attrgetter

auth = tweepy.OAuthHandler(access.consumer_key, access.consumer_secret)
auth.set_access_token(access.access_token, access.access_token_secret)

max_page_size = 200
max_tweets = 50000
max_return = 250

# Encapsulate operations on the active user
class Profile:

    twitter = tweepy.API(auth)
    max_page_size = 200
    max_tweets = 30000
    max_return = 250



    def __init__(self, sname):

        self.sname = sname
        self.user  = None


    # Paginate through the tweets retrieve them and apply filter and then sort them if needed
    def getTweets(self, f, limit=max_return):


        self.user = Profile.twitter.get_user(self.sname)
        mx = min(self.user.statuses_count, Profile.max_tweets)
        pages = int(math.ceil(float(mx)/Profile.max_page_size))
        tweets = []

        # Paginate
        for p in xrange(1, pages+1):
            tweets.extend([t for t in Profile.twitter.user_timeline(self.sname, count=Profile.max_page_size, page=p) if select(t, f) ])

        # Don't sort it if not needed 
        if validate(f.get('key')) == 'created_at':
            # Tweets are reversed by default
            if not f.get('reverse'):
                return [t._json for t in sorted(tweets, key=attrgetter(validate(f.get('key'))), reverse=(f.get('reverse')>0))][:limit]
        else:
            return [t._json for t in sorted(tweets, key=attrgetter(validate(f.get('key'))), reverse=(f.get('reverse')>0))][:limit]
            

        return [t._json for t in tweets[:limit]]


    # Get the profile of the Twitter handle associated with the user
    def getProfile(self):

        self.user = Profile.twitter.get_user(self.sname)
        return self.user._json

    # Validate the screen name
    def isValid(self):

        # Twitter handle can't be this long. Protect against any code injection attacks
        if len(self.sname) > 30:
            return False

        try:
            self.user = Profile.twitter.get_user(self.sname)
        except tweepy.TweepError, e:
            return False
        return True


    # Determine the score of a screen name.
    # Explore the partial follower graph one level down, wait if rate limitted.
    # Retreive a large number of tweets and determine the sentiment, wait if rate limitted.
    # Combine the different reputation components
    # Return and integer score
    def getScore(self):

        positive = 0
        negative = 0
        total = 0.0
        default_f = {   'photo':0,
                        'start': datetime.datetime.fromtimestamp(0),
                        'end': datetime.datetime.fromtimestamp(2147483647),
                        'key': 'some',
                        'reverse': 1
                    }

        tcalls = Profile.twitter.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
        print("Current rate limit on tweets %s" % (tcalls,))
        while tcalls < 150:
            time.sleep(5)
            tcalls = Profile.twitter.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
            print("Current rate limit on tweets %s" % (tcalls,))

        tweets = self.getTweets(default_f, limit=Profile.max_tweets)

        for tweet in tweets:
            (p, n, t) = score.parseTweet(tweet)
            positive += p
            negative += n
            total += t

        tcalls = Profile.twitter.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
        print("Current rate limit on tweets %s" % (tcalls,))

        ncalls = Profile.twitter.rate_limit_status()['resources']['followers']['/followers/list']['remaining']
        print("Current rate limit on followers graph %s" % (ncalls,))
        while ncalls < 10:
            time.sleep(5)
            ncalls = Profile.twitter.rate_limit_status()['resources']['followers']['/followers/list']['remaining']
            print("Current rate limit on followers graph %s" % (ncalls,))

        

        f_users = []
        for page in [f_page for f_page in tweepy.Cursor(Profile.twitter.followers, self.sname, count=200).pages(10)]:
            f_users.extend([f_user for f_user in page])

        f_scores = [score.scoreFollower(f_user) for f_user in f_users]

        self.score = score.scoreUser((positive, negative, total), self.user.followers_count, f_scores)

        ncalls = Profile.twitter.rate_limit_status()['resources']['followers']['/followers/list']['remaining']
        print("Current rate limit on followers graph %s" % (ncalls,))

        return self.score




        


# Filter helper
def select(tweet, f):
    
    # Photo filter
    if f.get('photo') is not 0:
        hasPhoto = False
        if tweet.entities.get('media'):
            for media in tweet.entities['media']:
                if media.get('type') == 'photo':
                    hasPhoto = True

        # Photo only
        if not hasPhoto and f.get('photo') > 0:
            return None

        # No Photo
        if hasPhoto and f.get('photo') < 0:
            return None

    # Timae range filter
    if tweet.created_at < f.get('start') or tweet.created_at > f.get('end'):
        return None

        
    return tweet

# Order key validation helper
def validate(key):

    # Sanitize the key
    validKeys = ['created_at', 'favorite_count', 'filter_level', 'retweet_count']
    if key not in validKeys:
        key = 'created_at'
    
    return key
