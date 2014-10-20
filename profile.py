import tweepy
import access

auth = tweepy.OAuthHandler(access.consumer_key, access.consumer_secret)
auth.set_access_token(access.access_token, access.access_token_secret)


class Profile:



    def __init__(self, user):
        self.user = user

    def getTweets(self):
        twitter = tweepy.API(auth)
        user = twitter.get_user(self.user)
        tweets = twitter.user_timeline(self.user, count=100)
        return tweets


    def getProfile(self):
        #TODO get profile
        return
