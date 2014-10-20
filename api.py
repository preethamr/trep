from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from profile import Profile

app = Flask(__name__)
api = Api(app)



def abort_if_user_doesnt_exist(user):
    if not isValid(user):
        abort(404, message="User {} doesn't exist".format(user))

# Argument validation
parser = reqparse.RequestParser()
parser.add_argument('user', type=str)

def userInfo(user):
    return Profile(user).getProfile()

def isValid(user):
    return True


# User profile
#   show a profile for a single twitter handle
class User(Resource):
    def get(self, user):
        abort_if_user_doesnt_exist(user)
        return userInfo(user)



# Tweets
#   shows a up to 100 tweets from start
class Tweets(Resource):
    def get(self, user, start, end):
        # TODO paginate with cursor
        return None


##
## Setup the Api resource routing here
##
# TODO #api.add_resource(Tweets, '/tweets')
api.add_resource(User, '/handle/<string:user>')


if __name__ == '__main__':
    app.run(debug=True)
