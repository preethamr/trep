from flask import Flask, jsonify
from flask.ext.cors import CORS
from flask.ext.restful import reqparse, abort, Api, Resource
from tprofile import Profile
import datetime
import json

app = Flask(__name__)
cors = CORS(app)
api = Api(app)




# Argument validation
parser = reqparse.RequestParser()
parser.add_argument('photo', type=int)
parser.add_argument('start', type=int)
parser.add_argument('end', type=int)
parser.add_argument('key', type=str)
parser.add_argument('reverse', type=int)

def userInfo(user):
    return Profile(user).getProfile()

def userTweets(user, f):
    return Profile(user).getTweets(f)

def isValid(user):
    return Profile(user).isValid()

def userScore(user):
    return Profile(user).getScore()


# User profile 
#   show a profile for a single twitter handle 
class User(Resource):
    def get(self, user):
        if not isValid(user):
            return jsonify(message="Twitter handle {} does not exist. Please try a valid Twitter handle.".format(user))
        return jsonify(userInfo(user))



# Tweets 
#   shows a up to 100 tweets from start 
class Tweets(Resource):
    def get(self, user):
        f = parser.parse_args()

        if not isValid(user):
            return jsonify(message="Twitter handle {} does not exist. Please try a valid Twitter handle.".format(user))

        if f['start']:
            f['start'] = datetime.datetime.fromtimestamp(f['start'])
        else:
            f['start'] = datetime.datetime.fromtimestamp(0)

        if f['end']:
            f['end'] = datetime.datetime.fromtimestamp(f['end'])
        else:
            f['end'] = datetime.datetime.fromtimestamp(2140483647)

        if f['photo'] is None:
            f['photo'] = 0

        if f['reverse'] is None:
            f['reverse'] = 1

        if f['key'] is None:
            f['key'] = 'created_at'

        print f
        return jsonify(tweets = userTweets(user, f))


# Score 
#   return score for a single twitter handle 
class Score(Resource):
    def get(self, user):
        if not isValid(user):
            return jsonify(message="Twitter handle {} does not exist. Please try a valid Twitter handle.".format(user))
        return jsonify(score = userScore(user))


##
## Setup the Api resource routing here
##
api.add_resource(Tweets, '/tweets/<string:user>', methods = ['GET'])
api.add_resource(User, '/profile/<string:user>', methods = ['GET'])
api.add_resource(Score, '/score/<string:user>', methods = ['GET'])


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
