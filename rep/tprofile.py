import access
import math
import tweepy

auth = tweepy.OAuthHandler(access.consumer_key, access.consumer_secret)
auth.set_access_token(access.access_token, access.access_token_secret)


class Profile:

    twitter = tweepy.API(auth)
    max_page_size = 200
    max_tweets = 2000



    def __init__(self, sname):
        self.sname = sname 

    def getTweets(self):
        user = Profile.twitter.get_user(self.sname)
        mx = max(user.statuses_count, Profile.max_tweets)
        pages = int(math.ceil(float(mx)/Profile.max_page_size))
        tweets = []

        # Paginate
        for p in xrange(1, pages+1):
            tweets.extend([t.text for t in Profile.twitter.user_timeline(self.sname, count=Profile.max_page_size, page=p)])

        return tweets

#        for tweet in public_tweets:
#            print tweet.text.encode('utf8')

    def getProfile(self):
        #TODO get profile
        user = Profile.twitter.get_user(self.sname)
        return user._json

    def isValid(self):
        try:
            user = Profile.twitter.get_user(self.sname)
        except tweepy.TweepError, e:
            return False
        return True
        
